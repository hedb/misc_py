import hou
import os
import sys
import json
import math

# --- Constants ---
DEFAULT_PARAMS_FILENAME = "parameters.json"
DEFAULT_OUTPUT_FILENAME = "scene_render.png"
DEFAULT_RES_X = 640
DEFAULT_RES_Y = 480

# --- Helper Functions ---

def load_parameters(filepath):
    """Loads parameters from a JSON file."""
    print(f"Loading parameters from: {filepath}")
    try:
        with open(filepath, 'r') as f:
            params = json.load(f)
        return params
    except FileNotFoundError:
        print(f"ERROR: Parameters file not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR loading parameters: {e}", file=sys.stderr)
        sys.exit(1)

def setup_scene():
    """Clears the scene and ensures essential contexts exist."""
    print("Clearing existing scene...")
    obj_context = hou.node("/obj")
    out_context = hou.node("/out")

    if obj_context is None:
        print("ERROR: /obj context not found!", file=sys.stderr)
        sys.exit(1)

    # Ensure /out exists
    if not out_context:
        out_context = hou.node("/").createNode("ropnet", "out")
        if out_context is None:
            print("ERROR: Failed to create /out context!", file=sys.stderr)
            sys.exit(1)
        print("Created /out context.")

    # Clear previous nodes
    for node in obj_context.children():
        node.destroy()
    for node in out_context.children():
        node.destroy()

    return obj_context, out_context

def create_base(obj_context, radius, height):
    """Creates the cylindrical base geometry."""
    print("Creating base geometry...")
    geo_node = obj_context.createNode("geo", "base_geo")
    if geo_node is None:
        print("ERROR: Failed to create base_geo node.", file=sys.stderr)
        return None # Indicate failure

    tube_sop = geo_node.createNode("tube", "base_cylinder")
    if tube_sop is None:
        print("ERROR: Failed to create tube SOP.", file=sys.stderr)
        return None

    # Configure the tube SOP
    tube_sop.parm("rad1").set(radius)
    tube_sop.parm("rad2").set(radius)
    tube_sop.parm("height").set(height)
    tube_sop.parm("cap").set(True)
    tube_sop.parm("ty").set(height / 2.0) # Center base bottom at Y=0

    # Add normals
    normal_sop = geo_node.createNode("normal", "add_normals")
    if normal_sop is None:
        print("WARNING: Failed to create normal SOP for base.", file=sys.stderr)
        # Allow continuing without normals, but set display on tube
        tube_sop.setDisplayFlag(True)
        tube_sop.setRenderFlag(True)
        return tube_sop # Return the last valid node
    else:
        normal_sop.setInput(0, tube_sop)
        normal_sop.setDisplayFlag(True)
        normal_sop.setRenderFlag(True)
        return normal_sop # Return the node to be rendered/displayed


# --- Rod Simulation Sub-Functions ---

def _create_initial_line(parent_node, rod_length, base_height):
    """Creates the initial straight line geometry."""
    print("  Creating initial rod line...")
    line_sop = parent_node.createNode("line", "initial_rod")
    if line_sop is None:
        print("  ERROR: Failed to create line SOP.", file=sys.stderr)
        return None
    try:
        line_sop.parm("originx").set(-rod_length / 2.0)
        line_sop.parm("originy").set(base_height)
        line_sop.parm("dirx").set(1)
        line_sop.parm("dist").set(rod_length)
        line_sop.parm("points").set(2) # Start with just endpoints
    except hou.Error as e:
        print(f"  ERROR setting line parameters: {e}", file=sys.stderr)
        return None
    return line_sop

def _resample_line(parent_node, input_line_sop, rod_length):
    """Resamples the line to add points for Vellum simulation."""
    print("  Resampling rod line...")
    resample_sop = parent_node.createNode("resample", "resample_rod")
    if resample_sop is None:
        print("  ERROR: Failed to create resample SOP.", file=sys.stderr)
        return None
    resample_sop.setInput(0, input_line_sop)

    measure_parm = resample_sop.parm("measure")
    length_parm = resample_sop.parm("length") # Param for segment length value

    if measure_parm is None or length_parm is None:
        print("  ERROR: Could not find 'measure' or 'length' parameters on Resample SOP.", file=sys.stderr)
        return None

    try:
        # Assume Index 1 corresponds to "Max. Segment Length" based on previous runs
        target_measure_index = 1
        measure_parm.set(target_measure_index)
        print(f"  Set 'measure' parameter using index: {target_measure_index}")

        # Set segment length value
        segment_length = rod_length / 50.0 # Example: 50 segments
        length_parm.set(segment_length)
        print(f"  Set segment length to: {segment_length}")
    except hou.Error as e:
         print(f"  ERROR setting Resample parameters: {e}", file=sys.stderr)
         return None
    return resample_sop

def _create_anchor_points(parent_node, base_radius, base_height):
    """Creates the two static anchor points on the base edge."""
    print("  Defining anchor points...")
    anchors_sop = parent_node.createNode("add", "anchor_points")
    if anchors_sop is None:
        print("  ERROR: Failed to create Add SOP for anchors.", file=sys.stderr)
        return None

    try:
        # --- FIX: Use correct parameter names pt0x, pt1x etc. ---
        anchors_sop.parm("points").set(2)
        anchors_sop.parm("pt0x").set(base_radius) # Point 0 (right side)
        anchors_sop.parm("pt0y").set(base_height)
        anchors_sop.parm("pt0z").set(0)

        anchors_sop.parm("pt1x").set(-base_radius) # Point 1 (left side)
        anchors_sop.parm("pt1y").set(base_height)
        anchors_sop.parm("pt1z").set(0)
        # --- END FIX ---
    except hou.Error as e:
         print(f"  ERROR setting Add SOP parameters for anchors: {e}", file=sys.stderr)
         return None
    return anchors_sop


def _setup_pinning_attributes(parent_node, input_rod_geo, input_anchor_geo):
    """Sets up groups and attributes needed for Vellum pin constraints using the standard 'group' SOP."""
    print("  Adding pinning attributes...")
    GROUP_NODE_TYPE_NAME = "group"
    print(f"  Attempting to create group node of type: '{GROUP_NODE_TYPE_NAME}'")
    rod_endpoints_group = parent_node.createNode(GROUP_NODE_TYPE_NAME, "rod_endpoints_grp")

    if rod_endpoints_group is None:
        print(f"  ERROR: Failed to create group node of type '{GROUP_NODE_TYPE_NAME}'.", file=sys.stderr)
        return None, None

    print(f"  Successfully created group node: {rod_endpoints_group.path()} of type {rod_endpoints_group.type().name()}")
    rod_endpoints_group.setInput(0, input_rod_geo)

    # --- DEBUG: List parameters (can be commented out later) ---
    # print(f"  Parameters available on '{rod_endpoints_group.path()}':")
    # try:
    #     param_names = [p.name() for p in rod_endpoints_group.parms()]
    #     param_names.sort()
    #     print(f"    {param_names}")
    # except Exception as e:
    #     print(f"    ERROR listing parameters: {e}", file=sys.stderr)
    # --- END DEBUG ---

    try:
        print("  Configuring 'group' SOP to select first and last points...")

        # 1. Set the name of the group to be created
        rod_endpoints_group.parm("crname").set("pin_targets")
        print(f"    Set 'crname' (created group name) to: 'pin_targets'")

        # 2. Set entity to Points
        # The 'entity' parameter on the 'group' SOP often takes string tokens like "points", "prims", etc.
        entity_parm = rod_endpoints_group.parm("entity")
        if entity_parm:
            try:
                entity_parm.set("points") # Try the string token
                print(f"    Set 'entity' to: 'points'")
            except hou.OperationFailed:
                # If token fails, try to find index from menu (though 'points' token is common)
                print(f"    Failed to set 'entity' to 'points' token. Listing menu items for 'entity':")
                try:
                    labels = entity_parm.menuLabels()
                    print(f"      Labels: {labels}")
                    points_idx = labels.index("Points")
                    entity_parm.set(points_idx)
                    print(f"      Set 'entity' to index {points_idx} (Points).")
                except (ValueError, hou.Error) as e_menu:
                    print(f"      ERROR finding/setting 'entity' to Points via menu: {e_menu}. Grouping might fail.", file=sys.stderr)
                    return None, None # Critical if we can't set to points
        else:
            print("    ERROR: 'entity' parameter not found.", file=sys.stderr)
            return None, None


        # 3. Enable "Keep by Number" section
        # The 'groupnumber' parameter has multiple "pages" or modes selected by an integer.
        # Mode 0 is "Disable", Mode 1 is "Enable Pattern", Mode 2 "Enable Start/End"
        # We want "Enable Pattern" which is usually index 1 for this switcher.
        groupnumber_switcher_parm = rod_endpoints_group.parm("groupnumber")
        if groupnumber_switcher_parm:
            groupnumber_switcher_parm.set(1) # Set to mode "Enable Pattern" (or "By Pattern")
            print(f"    Set 'groupnumber' switcher to mode 1 (Enable Pattern).")
        else:
            print("    ERROR: 'groupnumber' (switcher) parameter not found.", file=sys.stderr)
            return None, None


        # 4. Set the pattern to select points 0 and N-1
        pattern_parm = rod_endpoints_group.parm("pattern")
        if pattern_parm:
            num_points = input_rod_geo.geometry().numPoints()
            if num_points < 2:
                print("  ERROR: Input rod geometry has less than 2 points for grouping.", file=sys.stderr)
                return None, None
            pattern_string = f"0 {num_points - 1}"
            pattern_parm.set(pattern_string)
            print(f"    Set 'pattern' to: '{pattern_string}'")
        else:
            print(f"  ERROR: 'pattern' parameter not found.", file=sys.stderr)
            return None, None

    except hou.Error as e:
        print(f"  ERROR setting parameters for 'group' SOP: {e}", file=sys.stderr)
        print("  Check the parameter list and ensure the parameter names and values are correct for selecting first/last points.")
        return None, None

    # Add pin_idx attribute to anchors (this part should be fine)
    anchor_attr_sop = parent_node.createNode("attribwrangle", "anchor_pin_attr")
    if anchor_attr_sop is None:
        print("  ERROR: Failed to create 'attribwrangle' SOP for anchors.", file=sys.stderr)
        return None, None
    anchor_attr_sop.setInput(0, input_anchor_geo)
    anchor_attr_sop.parm("class").set("point")
    anchor_attr_sop.parm("snippet").set("i@pin_idx = @ptnum;")

    return rod_endpoints_group, anchor_attr_sop


def _setup_vellum_constraints(parent_node, input_geo_with_group, target_anchor_geo, rod_rigidness, base_radius):
    """Creates Vellum bend, stretch, and pin constraints."""
    print("  Setting up Vellum constraints...")
    last_constraint_node = input_geo_with_group

    # Bend Constraints
    vellum_bend_cons = parent_node.createNode("vellumconstraints", "rod_bend")
    if vellum_bend_cons is None: return None
    vellum_bend_cons.setInput(0, last_constraint_node)
    vellum_bend_cons.parm("constrainttype").set("bend")
    vellum_bend_cons.parm("group").set("pin_targets") # Apply to the rod points group
    vellum_bend_cons.parm("restlengthscale").set(1.0)
    vellum_bend_cons.parm("stiffness").set(rod_rigidness)
    vellum_bend_cons.parm("stiffnessexp").set(0)
    vellum_bend_cons.parm("thickness").set(base_radius * 0.03)
    last_constraint_node = vellum_bend_cons

    # Stretch Constraints
    vellum_stretch_cons = parent_node.createNode("vellumconstraints", "rod_stretch")
    if vellum_stretch_cons is None: return None
    vellum_stretch_cons.setInput(0, last_constraint_node)
    vellum_stretch_cons.parm("constrainttype").set("distance")
    vellum_stretch_cons.parm("grouptype").set("edges")
    vellum_stretch_cons.parm("stiffness").set(10000)
    vellum_stretch_cons.parm("stiffnessexp").set(0)
    last_constraint_node = vellum_stretch_cons

    # Pin Constraints
    vellum_pin_cons = parent_node.createNode("vellumconstraints", "rod_pin")
    if vellum_pin_cons is None: return None
    vellum_pin_cons.setInput(0, last_constraint_node)
    vellum_pin_cons.parm("constrainttype").set("pintoanimation")
    vellum_pin_cons.parm("group").set("pin_targets") # Group of points on rod to pin
    vellum_pin_cons.parm("targetgeo").set(target_anchor_geo.path()) # Anchor geometry
    vellum_pin_cons.parm("pintype").set(0)
    vellum_pin_cons.parm("matchattrib").set("pin_idx") # Match using attribute
    vellum_pin_cons.parm("restlength").set(0)
    last_constraint_node = vellum_pin_cons

    return last_constraint_node # Return the final constraint node

def _setup_vellum_solver(parent_node, geo_input, cons_input, coll_input, sim_params):
    """Creates and configures the Vellum solver."""
    print("  Setting up Vellum solver...")
    solver_sop = parent_node.createNode("vellumsolver", "solve_rod")
    if solver_sop is None: return None

    solver_sop.setInput(0, geo_input)       # Input Geometry (pre-constraints)
    solver_sop.setInput(1, cons_input)      # Constraints
    solver_sop.setInput(2, coll_input)      # Collision/Target Geometry

    try:
        substeps = sim_params.get("substeps", 10)
        constraint_iterations = sim_params.get("constraint_iterations", 100)
        solver_sop.parm("substeps").set(substeps)
        solver_sop.parm("constraintiterations").set(constraint_iterations)
        solver_sop.parm("force_startframe").set(True)
        solver_sop.parm("startframe").set(1)
    except hou.Error as e:
        print(f"  ERROR configuring Vellum solver: {e}", file=sys.stderr)
        return None
    return solver_sop

def _get_simulation_result(parent_node, solver_sop, settle_frames):
    """Creates an Object Merge to get the simulation result at a specific frame."""
    print(f"  Running simulation for {settle_frames} frames...")
    result_merge = parent_node.createNode("object_merge", "get_sim_result")
    if result_merge is None: return None

    result_merge.parm("objpath1").set(solver_sop.path())
    result_merge.parm("xformtype").set("local")
    result_merge.parm("frame").setExpression(f"{settle_frames}")

    try:
        # Force the node to cook to ensure it evaluates at the desired frame
        result_merge.cook(force=True, frame=settle_frames)
        print(f"  Simulation cooked up to frame {settle_frames}")
    except hou.Error as e:
         print(f"  ERROR cooking simulation result node: {e}", file=sys.stderr)
         return None
    return result_merge

def _add_final_thickness(parent_node, input_sim_geo, base_radius):
    """Adds thickness and normals to the final simulated geometry."""
    print("  Adding thickness to simulated rod...")
    polywire_sop = parent_node.createNode("polywire", "add_thickness")
    if polywire_sop is None: return None
    polywire_sop.setInput(0, input_sim_geo)
    try:
        polywire_sop.parm("radius").set(base_radius * 0.03)
    except hou.Error as e:
        print(f"  ERROR setting polywire radius: {e}", file=sys.stderr)
        return None # Or return polywire_sop?

    # Add normals
    normal_sop = parent_node.createNode("normal", "add_normals")
    if normal_sop is None:
        print("  WARNING: Failed to create final normal SOP.", file=sys.stderr)
        polywire_sop.setDisplayFlag(True)
        polywire_sop.setRenderFlag(True)
        return polywire_sop # Return previous node if normal fails
    else:
        normal_sop.setInput(0, polywire_sop)
        normal_sop.setDisplayFlag(True)
        normal_sop.setRenderFlag(True)
        return normal_sop


def create_and_simulate_rod_orchestrator(obj_context, base_radius, base_height, rod_length, rod_rigidness, sim_params):
    """Orchestrates the creation and simulation of a single bent rod using Vellum."""
    print(f"--- Starting Rod Simulation: Length={rod_length}, Rigidness={rod_rigidness} ---")

    # Basic validation
    if rod_length <= base_radius * 2:
        print(f"WARNING: Rod length ({rod_length}) may be too short for significant bending.", file=sys.stderr)

    # Create main container node
    rod_sim_geo = obj_context.createNode("geo", "rod_simulation")
    if rod_sim_geo is None:
        print("ERROR: Failed to create rod_simulation geo node.", file=sys.stderr)
        return None

    # --- Chain of Operations ---
    line_sop = _create_initial_line(rod_sim_geo, rod_length, base_height)
    if line_sop is None: return None

    resampled_line_sop = _resample_line(rod_sim_geo, line_sop, rod_length)
    if resampled_line_sop is None: return None

    anchors_sop = _create_anchor_points(rod_sim_geo, base_radius, base_height)
    if anchors_sop is None: return None

    rod_grouped_geo, anchors_with_attr = _setup_pinning_attributes(rod_sim_geo, resampled_line_sop, anchors_sop)
    if rod_grouped_geo is None or anchors_with_attr is None: return None

    final_constraint_node = _setup_vellum_constraints(rod_sim_geo, rod_grouped_geo, anchors_with_attr, rod_rigidness, base_radius)
    if final_constraint_node is None: return None

    # Note: Geo input to solver comes from *before* constraints were added
    solver_sop = _setup_vellum_solver(rod_sim_geo, rod_grouped_geo, final_constraint_node, anchors_with_attr, sim_params)
    if solver_sop is None: return None

    settle_frames = sim_params.get("settle_frames", 50)
    sim_result_node = _get_simulation_result(rod_sim_geo, solver_sop, settle_frames)
    if sim_result_node is None: return None

    final_display_node = _add_final_thickness(rod_sim_geo, sim_result_node, base_radius)
    if final_display_node is None: return None

    print("--- Rod simulation and geometry generation complete. ---")
    return final_display_node # Return the final node for rendering



def setup_camera_light(obj_context, base_radius, base_height, rod_length):
    """Creates and positions the camera and a default light."""
    print("Creating camera...")
    cam_node = obj_context.createNode("cam", "my_cam")
    if cam_node is None:
         print("ERROR: Failed to create camera.", file=sys.stderr)
         return None # Indicate failure

    # --- Camera Position Adjustment ---
    # Calculate a suitable distance back based on object radius and height
    # Use max(radius, height) for a simple estimate, add rod length, multiply by a factor
    object_span = max(base_radius * 2, base_height + rod_length)
    cam_distance = object_span * 2.5 # Pull back further (adjust multiplier as needed)
    cam_node.parm("tz").set(cam_distance)

    # Aim the camera towards the vertical center of the object
    aim_height = (base_height + rod_length) / 2.0
    cam_node.parm("ty").set(aim_height)

    # Keep a slight downward angle
    cam_node.parm("rx").set(-15)

    print(f"Camera positioned at tz={cam_distance:.2f}, ty={aim_height:.2f}, rx=-15")
    # --- End Adjustment ---


    print("Creating light...")
    light_node = obj_context.createNode("envlight", "my_env_light")
    if light_node is None:
        print("WARNING: Failed to create environment light.", file=sys.stderr)

    return cam_node # Return camera node for render setup


def setup_render_node(out_context, camera_path, output_path, res_x, res_y):
    """Creates and configures the OpenGL render node, with parameter listing."""
    print("Creating OpenGL ROP node...")
    rop_node = out_context.createNode("opengl", "my_opengl_render")

    if rop_node is None:
         print("ERROR: Failed to create OpenGL ROP node.", file=sys.stderr)
         return None
    print(f"OpenGL ROP Node created: {rop_node.path()}")

    # --- DEBUG: List all parameters ---
    print("-" * 20)
    print(f"Parameters available on {rop_node.path()} ({rop_node.type().name()}):")
    available_parms = []
    try:
        # Iterate through parameters and store their names
        for parm in rop_node.parms():
            available_parms.append(parm.name())
        # Sort alphabetically for easier reading
        available_parms.sort()
        # Print the list
        print(f"  {available_parms}")
    except Exception as e:
        print(f"  ERROR listing parameters: {e}", file=sys.stderr)
    print("-" * 20)
    # --- END DEBUG ---

    print("Configuring OpenGL ROP...")
    try:
        # Set camera and output path first (these are usually stable)
        camera_parm = rop_node.parm("camera")
        picture_parm = rop_node.parm("picture")

        if camera_parm:
            camera_parm.set(camera_path)
        else:
            print("ERROR: Could not find 'camera' parameter.", file=sys.stderr)
            return None

        if picture_parm:
            picture_parm.set(output_path)
        else:
            print("ERROR: Could not find 'picture' parameter.", file=sys.stderr)
            return None

        # Now, attempt to set resolution based on the printed list
        # Common names are 'tres' (toggle), 'override_camerares' (toggle), 'res_override' (toggle)
        # coupled with 'res1'/'res2' or 'resx'/'resy'
        # LOOK AT THE PRINTED LIST ABOVE and identify the correct names.
        # Replace the example names below with the actual ones found.

        # EXAMPLE - Replace 'DETECTED_OVERRIDE_PARAM_NAME' with the actual name
        detected_override_param_name = "tres" # <--- CHANGE THIS based on output list
        detected_resx_param_name = "res1"     # <--- CHANGE THIS based on output list
        detected_resy_param_name = "res2"     # <--- CHANGE THIS based on output list

        override_parm = rop_node.parm(detected_override_param_name)
        resx_parm = rop_node.parm(detected_resx_param_name)
        resy_parm = rop_node.parm(detected_resy_param_name)

        if override_parm and resx_parm and resy_parm:
            print(f"Attempting to set resolution override using '{detected_override_param_name}'...")
            override_parm.set(1) # Assuming it's a 0/1 toggle
            print(f"Attempting to set resolution using '{detected_resx_param_name}' and '{detected_resy_param_name}'...")
            resx_parm.set(res_x)
            resy_parm.set(res_y)
            print(f"Resolution set to {res_x}x{res_y}")
        else:
            print(f"WARNING: Could not find all expected resolution parameters ('{detected_override_param_name}', '{detected_resx_param_name}', '{detected_resy_param_name}'). Check list above. Rendering with default resolution.", file=sys.stderr)


        print("OpenGL ROP configured.")
        return rop_node

    except hou.Error as e:
        print(f"ERROR configuring OpenGL ROP node parameters: {e}", file=sys.stderr)
        return None
    except Exception as e: # Catch any other unexpected errors
         print(f"UNEXPECTED ERROR during ROP configuration: {e}", file=sys.stderr)
         return None


def render_scene(rop_node, output_path):
    """Triggers the render for the specified ROP node."""
    if rop_node is None:
        print("ERROR: Cannot render, ROP node is invalid.", file=sys.stderr)
        return False

    try:
        print(f"Rendering frame {int(hou.frame())} to {output_path}...")
        rop_node.render()
        print(f"--- Render SUCCESSFUL! ---")
        return True
    except hou.Error as e:
        print(f"--- Render FAILED: {e} ---", file=sys.stderr)
        return False
    except Exception as e: # Catch other potential errors
        print(f"--- UNEXPECTED RENDER ERROR: {e} ---", file=sys.stderr)
        return False

# --- Main Execution ---


def main():
    """Main function to orchestrate the script execution."""
    print("--- Houdini Lamp Rod Vellum Simulation Script ---")
    script_dir = os.path.dirname(os.path.realpath(__file__))
    params_path = os.path.join(script_dir, DEFAULT_PARAMS_FILENAME)

    # Load Parameters
    params = load_parameters(params_path)

    # Extract parameters
    base_params = params.get("base", {})
    base_radius = base_params.get("radius", 5.0)
    base_height = base_params.get("height", 3.0)

    rods_params = params.get("rods", {})
    rod_length = rods_params.get("length", 15.0) # Use the longer length
    rod_rigidness = rods_params.get("rigidness", 500) # Use stiffness

    render_params = params.get("render", {})
    output_filename = render_params.get("output_filename", "vellum_rod.png")
    res_x = render_params.get("resolution_x", DEFAULT_RES_X)
    res_y = render_params.get("resolution_y", DEFAULT_RES_Y)

    sim_params = params.get("simulation", {}) # Load simulation parameters

    output_path = os.path.join(script_dir, output_filename)
    output_path = os.path.abspath(output_path)
    print(f"Output path set to: {output_path}")
    print(f"Parameters loaded: Base Radius={base_radius}, Height={base_height}, Rod Length={rod_length}, Rigidness={rod_rigidness}")
    print(f"Simulation Params: {sim_params}")

    # Setup Scene
    obj_context, out_context = setup_scene()

    # Create Base Geometry
    base_render_node = create_base(obj_context, base_radius, base_height)
    if base_render_node is None:
         print("ERROR: Base geometry creation failed. Aborting.", file=sys.stderr)
         sys.exit(1)

    # --- Create and Simulate Rod ---
    
    rod_render_node = create_and_simulate_rod_orchestrator(obj_context, base_radius, base_height, rod_length, rod_rigidness, sim_params)
    #                                        ^^^^^^^^^^^^^^^
    if rod_render_node is None:
         print("ERROR: Rod simulation failed. Aborting.", file=sys.stderr)
         sys.exit(1)


    # Setup Camera and Light (Adjust for potentially bent rod)
    cam_node = setup_camera_light(obj_context, base_radius, base_height, base_radius) # Adjust aim slightly based on radius now
    if cam_node is None:
         print("ERROR: Camera setup failed. Aborting.", file=sys.stderr)
         sys.exit(1)

    # Setup Render Node
    rop_node = setup_render_node(out_context, cam_node.path(), output_path, res_x, res_y)
    if rop_node is None:
         print("ERROR: Render setup failed. Aborting.", file=sys.stderr)
         sys.exit(1)

    # Render Scene (This now renders frame 1, but geometry is result of simulation)
    # We force-cooked the result node earlier, so rendering frame 1 is okay.
    render_success = render_scene(rop_node, output_path)

    # Save Debug Scene
    debug_hip_filename = "debug_vellum_scene.hipnc"
    debug_hip_path = os.path.join(script_dir, debug_hip_filename)
    print(f"Saving debug scene to {debug_hip_path}...")
    try:
        hou.hipFile.save(debug_hip_path)
        print("Debug scene saved successfully.")
    except hou.Error as e:
        print(f"ERROR saving debug scene: {e}", file=sys.stderr)

    print("--- Script finished ---")
    if not render_success:
        sys.exit(1)


# --- Ensure all other function definitions (load_parameters, setup_scene, etc.) and the if __name__ == "__main__": block are still present ---
if __name__ == "__main__":
    main()