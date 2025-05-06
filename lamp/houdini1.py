import hou
import os
import sys

print("--- Houdini Hello World Render Script ---")

# --- Configuration ---
output_filename = "hello_houdini.png"
# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(script_dir, output_filename)
output_path = os.path.abspath(output_path) # Use absolute path for robustness

print(f"Output path set to: {output_path}")

# --- Scene Setup ---
# Get the object context node (where cameras, geo, lights live)
obj_context = hou.node("/obj")

# 1. Create Geometry
print("Creating geometry...")
geo_node = obj_context.createNode("geo", "my_sphere_geo") # Create a geometry container
sphere_node = geo_node.createNode("sphere") # Create a sphere SOP inside

# 2. Create Camera
print("Creating camera...")
cam_node = obj_context.createNode("cam", "my_cam")
# Position the camera slightly back
cam_node.parm("tz").set(5)

# 3. Create Light (using a simple environment light)
print("Creating light...")
# Use an environment light for simple overall illumination
light_node = obj_context.createNode("envlight", "my_env_light")
# Optional: Could set a simple HDR map if needed, but default works okay
# light_node.parm("env_map").set("path/to/your/default.hdr")

# --- Render Setup ---
# Get the ROPs context node (where render nodes live)
# Create it if it doesn't exist (it might not in a totally empty scene)
out_context = hou.node("/out")
if not out_context:
    print("Creating /out context...")
    out_context = hou.node("/").createNode("ropnet", "out") # ROP Network node

# 4. Create Render Node (OpenGL for speed)
print("Creating OpenGL ROP...")
# Note: For higher quality renders, you'd use "karma" or "ifd" (Mantra)
rop_node = out_context.createNode("opengl", "my_opengl_render")

# Configure the render node
print("Configuring ROP...")
# Set the camera to use
rop_node.parm("camera").set(cam_node.path()) # Use node.path() for safety

# Set the output picture path
# Use the 'picture' parameter specific to OpenGL ROP
rop_node.parm("picture").set(output_path)

# Optional: Set resolution (defaults are usually okay for test)
# rop_node.parm("res_override").set(1) # Enable resolution override
# rop_node.parm("res1").set(1280)
# rop_node.parm("res2").set(720)

# --- Trigger Render ---
try:
    print(f"Rendering frame {int(hou.frame())}...") # Renders the current frame
    rop_node.render()
    print(f"--- Render SUCCESSFUL! Image saved to: {output_path} ---")
except hou.Error as e:
    print(f"--- Render FAILED: {e} ---", file=sys.stderr)
    # In a real script, you might want to exit with an error code
    # sys.exit(1)

# Optional: You could save the Houdini scene file for debugging
# print("Saving debug scene...")
# hou.hipFile.save("hello_scene.hipnc")

print("--- Script finished ---")
