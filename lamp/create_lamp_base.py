import hou
import os
import sys
import json
import math
import datetime

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
    """Creates the initial curved line geometry that will be maintained by the physics."""
    print("  Creating initial rod line...")
    
    # Calculate base diameter for spacing the endpoints
    base_diameter = base_height * 2  # Using base height * 2 as a good reference
    
    # Create a simple line first - this should be compatible with all Houdini versions
    line_sop = parent_node.createNode("line", "rod_line")
    if line_sop is None:
        print("  ERROR: Failed to create line SOP.", file=sys.stderr)
        return None
        
    try:
        # Create a straight line that spans the base
        line_sop.parm("points").set(2)  # Just endpoints
        line_sop.parm("originx").set(-base_diameter/2)  # Start at left edge
        line_sop.parm("originy").set(base_height)      # At top of base
        line_sop.parm("originz").set(0)               # Centered
        
        line_sop.parm("dirx").set(1)                  # Direction along X axis
        line_sop.parm("diry").set(0)                  # No Y direction
        line_sop.parm("dirz").set(0)                  # No Z direction
        line_sop.parm("dist").set(base_diameter)      # Span across base
        
        # Add more points via resampling
        resample_sop = parent_node.createNode("resample", "divide_line")
        if resample_sop is None:
            return line_sop  # Return original line if resample fails
            
        resample_sop.setInput(0, line_sop)
        
        # Try different resampling parameter names
        if resample_sop.parm("method"):
            resample_sop.parm("method").set(0)  # By count
        
        # Set number of points
        num_points_param = None
        for param_name in ["npts", "points", "numsegments"]:
            if resample_sop.parm(param_name):
                num_points_param = param_name
                break
                
        if num_points_param:
            resample_sop.parm(num_points_param).set(40)  # More points for better bending
        else:
            return line_sop
            
        # Now add an attribute wrangle to push the points up to create a curved shape
        attrib_wrangle = parent_node.createNode("attribwrangle", "curve_up")
        if attrib_wrangle is None:
            return resample_sop
            
        attrib_wrangle.setInput(0, resample_sop)
        
        # Use simple attribute wrangling to push points up
        wrangle_code = '''
        // Create a parabolic curve by pushing middle points up
        float t = @ptnum / float(@numpt-1);  // normalized position along line
        float height = 2.0;                 // height multiplier
        
        // Push up in a parabolic shape (maximum at center)
        @P.y += height * (1.0 - pow(2.0*t - 1.0, 2));
        '''
        
        # Try to set the VEX code
        if attrib_wrangle.parm("snippet"):
            print("  Adding initial curve to rod using VEX")
            attrib_wrangle.parm("snippet").set(wrangle_code)
            return attrib_wrangle
        else:
            print("  WARNING: Could not set VEX snippet to curve line")
            return resample_sop
            
    except Exception as e:
        print(f"  ERROR setting line parameters: {e}", file=sys.stderr)
        return None

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
        # Create exactly 2 points
        anchors_sop.parm("points").set(2)
        
        # Make sure anchors match base_diameter
        base_diameter = base_height * 2  # Use base_height * 2 to match the curve
        
        # Position the first anchor at the left edge of the base top surface
        anchors_sop.parm("pt0x").set(-base_diameter/2)  # Left edge
        anchors_sop.parm("pt0y").set(base_height)       # At the top of the base
        anchors_sop.parm("pt0z").set(0)                # Centered in Z
        
        # Position the second anchor at the right edge of the base top surface
        anchors_sop.parm("pt1x").set(base_diameter/2)   # Right edge
        anchors_sop.parm("pt1y").set(base_height)       # At the top of the base
        anchors_sop.parm("pt1z").set(0)                # Centered in Z
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

    try:
        print("  Configuring 'group' SOP to select first and last points...")
        rod_endpoints_group.parm("crname").set("pin_targets")
        print(f"    Set 'crname' (created group name) to: 'pin_targets'")

        entity_parm = rod_endpoints_group.parm("entity")
        if entity_parm:
            try:
                entity_parm.set("points")
                print(f"    Set 'entity' to: 'points'")
            except hou.OperationFailed:
                print(f"    Failed to set 'entity' to 'points' token. Listing menu items for 'entity':")
                try:
                    labels = entity_parm.menuLabels()
                    print(f"      Labels: {labels}")
                    points_idx = labels.index("Points")
                    entity_parm.set(points_idx)
                    print(f"      Set 'entity' to index {points_idx} (Points).")
                except (ValueError, hou.Error) as e_menu:
                    print(f"      ERROR finding/setting 'entity' to Points via menu: {e_menu}. Grouping might fail.", file=sys.stderr)
                    return None, None
        else:
            print("    ERROR: 'entity' parameter not found.", file=sys.stderr)
            return None, None

        groupnumber_switcher_parm = rod_endpoints_group.parm("groupnumber")
        if groupnumber_switcher_parm:
            groupnumber_switcher_parm.set(1)
            print(f"    Set 'groupnumber' switcher to mode 1 (Enable Pattern).")
        else:
            print("    ERROR: 'groupnumber' (switcher) parameter not found.", file=sys.stderr)
            return None, None

        pattern_parm = rod_endpoints_group.parm("pattern")
        if pattern_parm:
            # Get geometry from the input node to the group SOP
            geo_to_group = input_rod_geo.geometry() # This is a hou.Geometry object
            if geo_to_group is None:
                print("  ERROR: Could not retrieve geometry from input_rod_geo.", file=sys.stderr)
                return None, None

            num_points = len(geo_to_group.points())

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
        return None, None

    # Add pin_idx attribute to anchors
    anchor_attr_sop = parent_node.createNode("attribwrangle", "anchor_pin_attr")
    if anchor_attr_sop is None:
        print("  ERROR: Failed to create 'attribwrangle' SOP for anchors.", file=sys.stderr)
        return None, None
    anchor_attr_sop.setInput(0, input_anchor_geo)
    anchor_attr_sop.parm("class").set("point")
    anchor_attr_sop.parm("snippet").set("i@pin_idx = @ptnum;")

    return rod_endpoints_group, anchor_attr_sop

def _print_constraint_type_menu(node, constraint_desc):
    """Helper to print the available menu items for 'constrainttype' parameter."""
    ctype_parm = node.parm("constrainttype")
    if ctype_parm:
        print(f"      --- Menu for 'constrainttype' on {node.path()} ({constraint_desc}) ---")
        try:
            labels = ctype_parm.menuLabels()
            print(f"        Labels: {labels}")
            for i, label in enumerate(labels):
                # Attempt to get token, but don't fail if it's not there
                token_str = "(Token N/A)"
                try:
                    token = ctype_parm.menuTokens()[i]
                    token_str = f"Token='{token}'"
                except (AttributeError, IndexError):
                    pass # Keep token_str as "(Token N/A)"
                print(f"        Index {i}: Label='{label}', {token_str}")
        except Exception as e_menu:
            print(f"        ERROR listing 'constrainttype' menu labels: {e_menu}")
        print(f"      --- End Menu for {constraint_desc} ---")
    else:
        print(f"      ERROR: 'constrainttype' parameter not found on {node.path()}", file=sys.stderr)

def _list_node_parameters(node, description="Node"):
    """Helper to print all parameters of a node."""
    print(f"      --- Parameters for {description} ({node.path()}) ---")
    try:
        parm_names = [p.name() for p in node.parms()]
        parm_names.sort()
        print(f"        {parm_names}")
    except Exception as e:
        print(f"        ERROR listing parameters: {e}")
    print(f"      --- End Parameters for {description} ---")

def _setup_vellum_constraints(parent_node, input_geo_with_group, target_anchor_geo, rod_rigidness, base_radius):
    """Creates Vellum bend, stretch, and pin constraints."""
    print("  Setting up Vellum constraints...")
    last_constraint_node_output = input_geo_with_group

    # --- Bend Constraints ---
    print("    Creating Vellum Bend constraints...")
    vellum_bend_cons_node = parent_node.createNode("vellumconstraints", "rod_bend")
    if vellum_bend_cons_node is None: 
        print("    ERROR: Failed to create Vellum Bend constraint node.", file=sys.stderr)
        return None
    vellum_bend_cons_node.setInput(0, last_constraint_node_output)
    try:
        vellum_bend_cons_node.parm("constrainttype").set("bend")
        
        # Use a higher stiffness to maintain the curved shape
        if vellum_bend_cons_node.parm("bendstiffness"):
            # Use a higher value to maintain the arc shape
            bend_stiffness = max(5000, rod_rigidness * 10.0)  # Increased 5x
            print(f"    Setting bend stiffness to {bend_stiffness}")
            vellum_bend_cons_node.parm("bendstiffness").set(bend_stiffness)
            
        # Set bend rest angles to preserve the initial curved shape
        if vellum_bend_cons_node.parm("bendrestscale"):
            vellum_bend_cons_node.parm("bendrestscale").set(1.0)  # Full rest scale
            
        # Minimal dampening to preserve the arc shape
        if vellum_bend_cons_node.parm("benddampingratio"):
            vellum_bend_cons_node.parm("benddampingratio").set(0.01)  # Low damping
            
        # Set bend type if available
        if vellum_bend_cons_node.parm("bendtype"):
            vellum_bend_cons_node.parm("bendtype").set(0)  # Default bend
            
    except hou.Error as e:
        print(f"    ERROR setting Vellum Bend constraint parameters: {e}", file=sys.stderr)
        return None
    last_constraint_node_output = vellum_bend_cons_node

    # --- Stretch Constraints ---
    print("    Creating Vellum Stretch constraints...")
    vellum_stretch_cons_node = parent_node.createNode("vellumconstraints", "rod_stretch")
    if vellum_stretch_cons_node is None: 
        print("    ERROR: Failed to create Vellum Stretch constraint node.", file=sys.stderr)
        return None
    vellum_stretch_cons_node.setInput(0, last_constraint_node_output)
    try:
        vellum_stretch_cons_node.parm("constrainttype").set("distance")
        vellum_stretch_cons_node.parm("grouptype").set("edges")
        
        # Higher stretch stiffness to prevent the rod from stretching
        if vellum_stretch_cons_node.parm("stretchstiffness"):
            stretch_stiffness = 100000  # Extreme stiffness
            print(f"    Setting stretch stiffness to {stretch_stiffness}")
            vellum_stretch_cons_node.parm("stretchstiffness").set(stretch_stiffness)
            
        # Keep shape stable with less stretching in compression
        if vellum_stretch_cons_node.parm("compressstiffness"):
            vellum_stretch_cons_node.parm("compressstiffness").set(100000)  # High compression resistance
            
    except hou.Error as e:
        print(f"    ERROR setting Vellum Stretch constraint parameters: {e}", file=sys.stderr)
        return None
    last_constraint_node_output = vellum_stretch_cons_node

    # --- Pin Constraints ---
    print("    Creating Vellum Pin constraints...")
    vellum_pin_cons_node = parent_node.createNode("vellumconstraints", "rod_pin")
    if vellum_pin_cons_node is None: return None
    vellum_pin_cons_node.setInput(0, last_constraint_node_output)

    try:
        # Set constraint type
        vellum_pin_cons_node.parm("constrainttype").set("pin")
        
        # Set target group
        vellum_pin_cons_node.parm("group").set("pin_targets")
        
        # Set target path
        targetpath_parm = vellum_pin_cons_node.parm("targetpath")
        if targetpath_parm:
            targetpath_parm.set(target_anchor_geo.path())
        else:
            print("      ERROR: 'targetpath' parameter not found for Pin constraint.", file=sys.stderr)
            return None

        # Set pin type to permanent with high stiffness
        pintype_parm = vellum_pin_cons_node.parm("pintype")
        if pintype_parm:
            pintype_parm.set(0)  # Permanent
        else:
            print("      ERROR: 'pintype' parameter not found.", file=sys.stderr)
            return None
            
        # Set pin stiffness if available
        if vellum_pin_cons_node.parm("pinstiffness"):
            pin_stiffness = 50000  # Extreme pinning
            print(f"    Setting pin stiffness to {pin_stiffness}")
            vellum_pin_cons_node.parm("pinstiffness").set(pin_stiffness)

        # Enable matching animation
        matchanim_parm = vellum_pin_cons_node.parm("matchanimation")
        if matchanim_parm:
            matchanim_parm.set(1)  # Enable
        
        # Set rest length if parameter exists - 0 means exact pinning
        restlength_parm = vellum_pin_cons_node.parm("restlength")
        if restlength_parm:
            restlength_parm.set(0)

    except hou.Error as e:
        print(f"    ERROR setting Vellum Pin constraint parameters: {e}", file=sys.stderr)
        return None
    except Exception as e_unexp:
        print(f"    UNEXPECTED ERROR setting Vellum Pin constraints: {e_unexp}", file=sys.stderr)
        return None

    return vellum_pin_cons_node

def _setup_vellum_solver(parent_node, geo_input, cons_input, coll_input, sim_params):
    """Creates and configures the Vellum solver."""
    print("  Setting up Vellum solver...")
    solver_sop = parent_node.createNode("vellumsolver", "solve_rod")
    if solver_sop is None: return None

    solver_sop.setInput(0, geo_input)       # Input Geometry (pre-constraints)
    solver_sop.setInput(1, cons_input)      # Constraints
    solver_sop.setInput(2, coll_input)      # Collision/Target Geometry

    try:
        # Increase substeps and iterations for more stable simulation
        substeps = sim_params.get("substeps", 30)  # Increased from 15
        constraint_iterations = sim_params.get("constraint_iterations", 250)  # Increased from 200
        
        # Check if parameters exist before setting them
        substeps_parm = solver_sop.parm("substeps")
        if substeps_parm:
            substeps_parm.set(substeps)
            print(f"    Set substeps to {substeps}")
        
        # Try different parameters for constraint iterations
        iterations_parm = solver_sop.parm("constraintiterations")
        if not iterations_parm:
            iterations_parm = solver_sop.parm("iterations")
            
        if iterations_parm:
            iterations_parm.set(constraint_iterations)
            print(f"    Set constraint iterations to {constraint_iterations}")
        
        # Set start frame parameters if they exist
        startframe_toggle = solver_sop.parm("force_startframe")
        if startframe_toggle:
            startframe_toggle.set(True)
        
        startframe_parm = solver_sop.parm("startframe")
        if startframe_parm:
            startframe_parm.set(1)
            
        # Disable gravity for this shape - we want to maintain the curved shape
        # without being pulled down by gravity
        if solver_sop.parm("gravityscale"):
            solver_sop.parm("gravityscale").set(0.0)  # Turn off gravity
            print("    Disabled gravity using gravityscale")
        elif solver_sop.parm("gravityy"):
            solver_sop.parm("gravityy").set(0.0)  # Alternative way to disable gravity
            print("    Disabled gravity using gravityy")
            
        # Set appropriate stiffness/damping for the material
        if solver_sop.parm("posdamp"):
            solver_sop.parm("posdamp").set(0.1)  # Lower damping to allow movement
            
        # Enable rest shape preservation (maintains initial shape)
        if solver_sop.parm("doprestshape"):
            solver_sop.parm("doprestshape").set(1)  # Enable rest shape
            print("    Enabled rest shape preservation")
        
        # If there's a restshapestiffness parameter, set it to maintain shape
        if solver_sop.parm("restshapestiffness"):
            solver_sop.parm("restshapestiffness").set(1.0)  # Maximum tendency to keep shape
            print("    Set rest shape stiffness to maximum")
        
        # Check for pressure parameters - might help with stability
        if solver_sop.parm("dopressure"):
            solver_sop.parm("dopressure").set(1)  # Enable pressure
            print("    Enabled pressure")
            
            if solver_sop.parm("pressure"):
                solver_sop.parm("pressure").set(1.0)  # Set pressure value
                print("    Set pressure to 1.0")
        
    except hou.Error as e:
        print(f"  ERROR configuring Vellum solver: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  UNEXPECTED ERROR configuring Vellum solver: {e}", file=sys.stderr)
        return None
        
    return solver_sop

def _get_simulation_result(parent_node, solver_sop, settle_frames):
    """Creates an Object Merge to get the simulation result at a specific frame."""
    print(f"  Running simulation for {settle_frames} frames...")
    
    # First create some debug outputs at different frames
    for frame in [10, 25, 50, 75, settle_frames]:
        debug_merge = parent_node.createNode("object_merge", f"frame_{frame}_result")
        if debug_merge is None:
            continue
            
        # Set the object path to merge from
        if debug_merge.parm("objpath1"):
            debug_merge.parm("objpath1").set(solver_sop.path())
            
        # Try different methods to set the frame
        frame_set = False
        for frame_param in ["frame", "f", "frame_number", "framenum"]:
            frame_parm = debug_merge.parm(frame_param)
            if frame_parm:
                try:
                    frame_parm.set(frame)
                    frame_set = True
                    break
                except:
                    pass
                    
        if not frame_set:
            print(f"  WARNING: Could not set frame parameter for debug merge at frame {frame}")
    
    # Create the final result merge
    result_merge = parent_node.createNode("object_merge", "get_sim_result")
    if result_merge is None: 
        print("  ERROR: Failed to create object_merge node.", file=sys.stderr)
        return None

    # Set the object path to merge from
    objpath_parm = result_merge.parm("objpath1")
    if objpath_parm:
        objpath_parm.set(solver_sop.path())
    else:
        print("  ERROR: 'objpath1' parameter not found on object_merge node.", file=sys.stderr)
        return None
    
    # Set transform type to local
    xform_parm = result_merge.parm("xformtype")
    if xform_parm:
        xform_parm.set("local")
    
    # Set the frame to read from
    frame_parm = result_merge.parm("frame")
    if frame_parm:
        try:
            frame_parm.setExpression(f"{settle_frames}")
        except hou.Error:
            try:
                frame_parm.set(settle_frames)
            except hou.Error as e:
                print(f"  ERROR setting frame parameter: {e}", file=sys.stderr)
                return None
    else:
        # Try alternative parameter names
        alt_params = ["f", "frame_number", "framenum"]
        param_found = False
        
        for alt_name in alt_params:
            alt_parm = result_merge.parm(alt_name)
            if alt_parm:
                try:
                    alt_parm.set(settle_frames)
                    param_found = True
                    print(f"  Set frame to {settle_frames} using parameter '{alt_name}'")
                    break
                except hou.Error:
                    pass
        
        if not param_found:
            print("  WARNING: Could not find any frame parameter to set.")

    try:
        # Try to set current frame first, then cook
        try:
            if hasattr(hou, 'setFrame'):
                hou.setFrame(settle_frames)
                print(f"  Set Houdini current frame to {settle_frames}")
            elif hasattr(hou, 'frame') and callable(hou.frame):
                hou.frame(settle_frames)
                print(f"  Set Houdini current frame to {settle_frames} using hou.frame()")
        except Exception as e:
            print(f"  WARNING: Could not set current frame: {e}")
            
        # Now cook
        result_merge.cook(force=True)
        print("  Cooked simulation result node")
    except hou.Error as e:
        print(f"  ERROR cooking simulation result node: {e}", file=sys.stderr)
        print("  Continuing with unchecked merge node...")
    
    return result_merge

def _add_final_thickness(parent_node, input_sim_geo, base_radius):
    """Adds thickness and normals to the final simulated geometry."""
    print("  Adding thickness to simulated rod...")
    polywire_sop = parent_node.createNode("polywire", "add_thickness")
    if polywire_sop is None: return None
    polywire_sop.setInput(0, input_sim_geo)
    try:
        # Increase the rod thickness to be more visible
        # Use a fixed thickness that's proportional to the base
        rod_radius = base_radius * 0.15  # Much thicker than before (was 0.03)
        polywire_sop.parm("radius").set(rod_radius)
        
        # Use more divisions for a smoother rod
        if polywire_sop.parm("divisions"):
            polywire_sop.parm("divisions").set(12)  # Higher quality divisions
            
        # Make it a round profile
        if polywire_sop.parm("type"):
            polywire_sop.parm("type").set(0)  # Round profile
    except hou.Error as e:
        print(f"  ERROR setting polywire radius: {e}", file=sys.stderr)
        return None

    # Add normals
    normal_sop = parent_node.createNode("normal", "add_normals")
    if normal_sop is None:
        print("  WARNING: Failed to create final normal SOP.", file=sys.stderr)
        polywire_sop.setDisplayFlag(True)
        polywire_sop.setRenderFlag(True)
        return polywire_sop # Return previous node if normal fails
    else:
        normal_sop.setInput(0, polywire_sop)
        
        # Add some material/color properties to make it more visible
        material_sop = parent_node.createNode("material", "rod_material")
        if material_sop is None:
            normal_sop.setDisplayFlag(True)
            normal_sop.setRenderFlag(True)
            return normal_sop
            
        material_sop.setInput(0, normal_sop)
        
        # Set material properties if available
        if material_sop.parm("diffr"):
            # Set a bright red color for the rod
            material_sop.parm("diffr").set(1.0)  # Full red
            material_sop.parm("diffg").set(0.0)  # No green
            material_sop.parm("diffb").set(0.0)  # No blue
            
            # Make it slightly glossy
            if material_sop.parm("specr"):
                material_sop.parm("specr").set(0.8)
                material_sop.parm("specg").set(0.8)
                material_sop.parm("specb").set(0.8)
                
            if material_sop.parm("rough"):
                material_sop.parm("rough").set(0.2)  # Fairly smooth surface
                
        material_sop.setDisplayFlag(True)
        material_sop.setRenderFlag(True)
        return material_sop

    return normal_sop

def create_and_simulate_rod_orchestrator(obj_context, base_radius, base_height, rod_length, rod_rigidness, sim_params):
    """Orchestrates the creation and simulation of a single bent rod using Vellum."""
    print(f"--- Starting Rod Simulation: Length={rod_length}, Rigidness={rod_rigidness} ---")

    if rod_length <= base_radius * 2:
        print(f"WARNING: Rod length ({rod_length}) may be too short for significant bending.", file=sys.stderr)

    rod_sim_geo = obj_context.createNode("geo", "rod_simulation")
    if rod_sim_geo is None: return None

    line_sop = _create_initial_line(rod_sim_geo, rod_length, base_height)
    if line_sop is None: return None

    resampled_line_sop = _resample_line(rod_sim_geo, line_sop, rod_length)
    if resampled_line_sop is None: return None

    anchors_sop = _create_anchor_points(rod_sim_geo, base_radius, base_height)
    if anchors_sop is None: return None

    # rod_grouped_geo is the resampled line with the 'pin_targets' group on its endpoints.
    # anchors_with_attr is the anchor points geometry with the 'pin_idx' attribute.
    rod_grouped_geo_node, anchors_with_attr_node = _setup_pinning_attributes(rod_sim_geo, resampled_line_sop, anchors_sop)
    if rod_grouped_geo_node is None or anchors_with_attr_node is None: return None

    # final_constraint_node is the last vellumconstraints SOP in the chain (e.g., vellum_pin_cons_node)
    # It carries the constraint information.
    # The geometry that the constraints apply to is rod_grouped_geo_node.
    final_constraint_node = _setup_vellum_constraints(rod_sim_geo, rod_grouped_geo_node, anchors_with_attr_node, rod_rigidness, base_radius)
    if final_constraint_node is None: return None

    # --- CORRECTED SOLVER INPUTS ---
    # Input 0: Geometry to simulate (the rod with the group for pinning)
    # Input 1: Constraints (output of the last vellumconstraints node)
    # Input 2: Collision/Target Geometry (the anchor points for pinning)
    solver_sop = _setup_vellum_solver(rod_sim_geo, rod_grouped_geo_node, final_constraint_node, anchors_with_attr_node, sim_params)
    # --- END CORRECTION ---
    if solver_sop is None: return None

    settle_frames = sim_params.get("settle_frames", 50)
    sim_result_node = _get_simulation_result(rod_sim_geo, solver_sop, settle_frames)
    if sim_result_node is None: return None

    final_display_node = _add_final_thickness(rod_sim_geo, sim_result_node, base_radius)
    if final_display_node is None: return None

    print("--- Rod simulation and geometry generation complete. ---")
    return final_display_node

def setup_camera_light(obj_context, base_radius, base_height, rod_length):
    """Creates and positions the camera and a default light."""
    print("Creating camera...")
    cam_node = obj_context.createNode("cam", "my_cam")
    if cam_node is None:
         print("ERROR: Failed to create camera.", file=sys.stderr)
         return None # Indicate failure

    # --- Camera Position Adjustment ---
    # Calculate a suitable distance based on object dimensions
    object_span = max(base_radius * 3, base_height + rod_length)
    cam_distance = object_span * 2.0  # Position camera back enough to see the entire scene
    
    # Position camera more isometrically to view the bend better
    cam_node.parm("tx").set(cam_distance * 0.6)  # Offset in X for isometric view
    cam_node.parm("ty").set(base_height + rod_length * 0.4)  # Position camera height to see the bend
    cam_node.parm("tz").set(cam_distance * 0.8)  # Offset in Z for isometric view

    # Aim the camera towards the base center
    # Use lookat parameters if available
    if cam_node.parm("lookat"):
        cam_node.parm("lookat").set(1)  # Enable lookat
        if cam_node.parm("lookatx"):
            cam_node.parm("lookatx").set(0)  # Center X
        if cam_node.parm("lookaty"):
            cam_node.parm("lookaty").set(base_height * 0.6)  # Slightly above base center
        if cam_node.parm("lookatz"):
            cam_node.parm("lookatz").set(0)  # Center Z
    else:
        # Otherwise use rotation
        cam_node.parm("rx").set(-20)  # Look down
        cam_node.parm("ry").set(-45)  # Rotate for isometric view
        cam_node.parm("rz").set(0)

    print(f"Camera positioned for isometric view")

    print("Creating light...")
    light_node = obj_context.createNode("envlight", "my_env_light")
    if light_node is None:
        print("WARNING: Failed to create environment light.", file=sys.stderr)
    else:
        # Position light above and to the side for nice shadows
        light_node.parm("tx").set(base_radius * 2)
        light_node.parm("ty").set(base_height + rod_length)
        light_node.parm("tz").set(-base_radius * 2)
        
        # Aim light towards base
        light_node.parm("lookat").set(1) if light_node.parm("lookat") else None
        light_node.parm("lookatx").set(0) if light_node.parm("lookatx") else None
        light_node.parm("lookaty").set(base_height * 0.5) if light_node.parm("lookaty") else None
        light_node.parm("lookatz").set(0) if light_node.parm("lookatz") else None
        
        # Increase light intensity
        light_node.parm("intensity").set(1.5) if light_node.parm("intensity") else None

    return cam_node # Return camera node for render setup


def setup_render_node(out_context, camera_path, output_path, res_x, res_y):
    """Creates and configures the OpenGL render node."""
    print("Creating OpenGL ROP node...")
    rop_node = out_context.createNode("opengl", "my_opengl_render")

    if rop_node is None:
         print("ERROR: Failed to create OpenGL ROP node.", file=sys.stderr)
         return None
    print(f"OpenGL ROP Node created: {rop_node.path()}")

    # Debug parameter listing - can be disabled or removed when not needed
    if False:  # Set to True if debugging is needed
        print("-" * 20)
        print(f"Parameters available on {rop_node.path()} ({rop_node.type().name()}):")
        try:
            available_parms = []
            for parm in rop_node.parms():
                available_parms.append(parm.name())
            available_parms.sort()
            print(f"  {available_parms}")
        except Exception as e:
            print(f"  ERROR listing parameters: {e}", file=sys.stderr)
        print("-" * 20)

    print("Configuring OpenGL ROP...")
    try:
        # Set camera and output path
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

        # Set resolution override
        override_parm = rop_node.parm("tres")
        resx_parm = rop_node.parm("res1")
        resy_parm = rop_node.parm("res2")

        if override_parm and resx_parm and resy_parm:
            override_parm.set(1)
            resx_parm.set(res_x)
            resy_parm.set(res_y)
            print(f"Resolution set to {res_x}x{res_y}")
        else:
            print(f"WARNING: Could not set resolution. Rendering with default resolution.", file=sys.stderr)

        print("OpenGL ROP configured.")
        return rop_node

    except hou.Error as e:
        print(f"ERROR configuring OpenGL ROP node parameters: {e}", file=sys.stderr)
        return None
    except Exception as e:
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
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(script_dir, "scene_output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Load Parameters
    params = load_parameters(params_path)

    # Extract parameters
    base_params = params.get("base", {})
    base_radius = base_params.get("radius", 5.0)
    base_height = base_params.get("height", 3.0)

    rods_params = params.get("rods", {})
    rod_length = rods_params.get("length", 25.0) # Shorter rod length to make bending more visible
    rod_rigidness = rods_params.get("rigidness", 5000) # Much higher rigidness

    render_params = params.get("render", {})
    output_filename = render_params.get("output_filename", "bent_rod_render.png")
    res_x = render_params.get("resolution_x", 800)  # Higher resolution for better visibility
    res_y = render_params.get("resolution_y", 600)

    # Set improved simulation parameters
    sim_params = params.get("simulation", {})
    if "settle_frames" not in sim_params:
        sim_params["settle_frames"] = 100  # More frames for stable simulation
    if "substeps" not in sim_params:
        sim_params["substeps"] = 30  # More substeps for accuracy
    if "constraint_iterations" not in sim_params:
        sim_params["constraint_iterations"] = 250  # More iterations for better constraint solving

    # Update paths to use output directory
    output_path = os.path.join(output_dir, output_filename)
    output_path = os.path.abspath(output_path)
    print(f"Output image will be saved to: {output_path}")
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

    # Save scene with timestamp
    timestamp = datetime.datetime.now().strftime("%H_%M_%S")
    scene_filename = f"lamp_rod_{timestamp}.hipnc"
    scene_path = os.path.join(output_dir, scene_filename)
    print(f"Saving scene to {scene_path}...")
    try:
        hou.hipFile.save(scene_path)
        print("Scene saved successfully with timestamp.")
    except hou.Error as e:
        print(f"ERROR saving scene: {e}", file=sys.stderr)
        scene_path = None

    # Try to open the saved file in Houdini
    if scene_path and os.path.exists(scene_path):
        try:
            # Determine the OS and use appropriate command
            if sys.platform == 'darwin':  # macOS
                open_cmd = f"open \"{scene_path}\""
                print(f"Opening scene with command: {open_cmd}")
                os.system(open_cmd)
            elif sys.platform == 'win32':  # Windows
                open_cmd = f"start \"\" \"{scene_path}\""
                print(f"Opening scene with command: {open_cmd}")
                os.system(open_cmd)
            elif sys.platform.startswith('linux'):  # Linux
                open_cmd = f"xdg-open \"{scene_path}\""
                print(f"Opening scene with command: {open_cmd}")
                os.system(open_cmd)
            else:
                print(f"Auto-opening of scene file not supported on platform: {sys.platform}")
                print(f"Please open the file manually at: {scene_path}")
        except Exception as e:
            print(f"WARNING: Could not open scene file automatically: {e}", file=sys.stderr)
            print(f"Please open the file manually at: {scene_path}")
    else:
        print("Scene file not found, cannot open automatically.")

    print("--- Script finished ---")


# --- Ensure all other function definitions (load_parameters, setup_scene, etc.) and the if __name__ == "__main__": block are still present ---
if __name__ == "__main__":
    main()