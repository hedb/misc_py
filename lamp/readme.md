# Houdini Parametric Lamp Rod Simulator

## 1. Aim of the Project
This project aims to create a Python-scripted tool that leverages Houdini's Vellum physics engine to simulate the shape of a semi-rigid rod when its ends are constrained to a circular base. The goal is to explore how different parameters (base size, rod length, rod stiffness) affect the final bent curvature of the rod.

The ultimate vision is to extend this to simulate more complex lamp structures where multiple such rods give shape to a cloth manifold. This initial phase focuses on parametrically generating and simulating a single rod element.

The tool is designed to be run headlessly (without the Houdini GUI), taking input parameters from a JSON file and outputting a rendered image of the simulated shape, as well as a Houdini scene file (.hipnc) for inspection and debugging.

## 2. Code Description (High Level)
The system is driven by a main Python script (`create_lamp_base.py`) that utilizes Houdini's Python API (`hou` module) when executed with `hython` (Houdini's Python interpreter).

### Workflow:

#### Parameter Loading (`load_parameters`):
- Reads a `parameters.json` file. This file defines:
  - `base`: Dimensions (radius, height) of the cylindrical base.
  - `rods`: Properties of the rod (length, rigidness).
  - `simulation`: Parameters for the Vellum solver (settle frames, substeps, constraint iterations).
  - `render`: Output image filename and resolution.

#### Scene Setup (`setup_scene`):
- Clears any existing nodes from the Houdini scene to ensure a clean run.
- Ensures necessary contexts like `/obj` (objects) and `/out` (render operators) exist.

#### Base Geometry Creation (`create_base`):
- Creates a cylindrical mesh representing the lamp base using a Tube SOP, configured according to the JSON parameters.

#### Rod Geometry Generation and Vellum Simulation (`create_and_simulate_rod_orchestrator` and its sub-functions):
This is the core of the simulation. It's broken down into several steps, managed within a dedicated geometry node (`/obj/rod_simulation`):

1. **Initial Line** (`_create_initial_line`): A straight line SOP is created, positioned at the base height and spanning longer than the base diameter.

2. **Resampling** (`_resample_line`): The line is resampled to add more points along its length for accurate Vellum simulation.

3. **Anchor Points** (`_create_anchor_points`): Two points are created positioned on opposite edges of the top surface of the base to serve as static targets.

4. **Pinning Attributes** (`_setup_pinning_attributes`):
   - A point group (`pin_targets`) is created on the resampled rod, selecting its first and last points.
   - An integer attribute `pin_idx` is added to the two anchor points.

5. **Vellum Constraints** (`_setup_vellum_constraints`):
   - **Bend Constraints**: Applied to the rod, using the `rod_rigidness` parameter to control its stiffness.
   - **Stretch Constraints**: Applied to the rod to maintain its segment lengths (making it behave like a semi-rigid wire).
   - **Pin Constraints**: Configured to pin the rod ends to the anchor points, using the `pin_idx` attribute for matching.

6. **Vellum Solver Setup** (`_setup_vellum_solver`): A Vellum Solver SOP is created and configured with substeps and iterations parameters.

7. **Simulation & Result Extraction** (`_get_simulation_result`): The simulation is run for the specified number of frames, and the final state is captured.

8. **Final Thickness** (`_add_final_thickness`): The simulated (bent) rod geometry is given thickness for rendering.

#### Camera and Light Setup (`setup_camera_light`):
- A camera is created and positioned to frame the generated base and simulated rod.
- A simple environment light is added for basic illumination.

#### Render Setup (`setup_render_node`):
- An OpenGL ROP (Render OPerator) is configured with the camera and output settings.

#### Rendering (`render_scene`):
- The OpenGL ROP is triggered to render the scene to an image file.

#### Save Scene File (in `main` function):
- The entire Houdini scene is saved to a `.hipnc` file for later inspection.

### Error Handling and Compatibility:
The code includes robust error handling mechanisms:
- Parameter validation for all Houdini node operations
- Fallbacks for different Houdini versions with varying parameter names
- Clear error messages to aid in diagnosing issues
- Graceful recovery when possible to continue execution

### Key Houdini Concepts Used:
- **SOPs (Surface OPerators)**: Line, Tube, Resample, Add, Group, PolyWire, Object Merge, AttribWrangle
- **Vellum**: Vellum Constraints SOP (for Bend, Stretch, Pin), Vellum Solver SOP
- **Python Scripting** (`hou` module): Node creation, parameter setting, process automation
- **ROPs (Render OPerators)**: OpenGL ROP

## 3. Usage
1. Ensure Houdini is installed (tested with Houdini 20.5)
2. Configure parameters in `parameters.json`
3. Run via command line: `hython create_lamp_base.py`
4. Output will be saved to the `scene_output` directory:
   - Rendered image: Based on filename in `parameters.json`
   - Houdini scene file: `debug_vellum_scene.hipnc`

## 4. Directory Structure
```
lamp/
├── create_lamp_base.py    # Main script
├── parameters.json        # Configuration file
├── setup_houdini_env.sh   # Houdini environment setup
├── readme.md              # This documentation
└── scene_output/          # Output directory
    ├── [rendered_image]   # Rendered output (filename from parameters.json)
    └── debug_vellum_scene.hipnc  # Saved Houdini scene for inspection
```

## 5. Dependencies
- Houdini (20.5 or compatible version)
- Python 3.x with Houdini's Python API
