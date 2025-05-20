from world_objects import World, StretchFunction
from sheet import Sheet

def main():
    # Initialize the world with gravity
    # World.the_world = None # No longer needed due to World.reset() or World.init_world()
    world = World.init_world(gravity_accel=(0, 0, -0.5)) # Use init_world or reset
    # To reset in subsequent runs or clear state: world = World.reset(gravity_accel=(0,0,-0.5))
    
    # Create a stretch function for the edges
    stretch = StretchFunction(func_type="linear", rest_length=1.0, unit_inc=1.0)
    
    # Create a sheet in the XY plane
    sheet1 = Sheet(
        hex_count=(5, 5),  # Smaller sheet for better visualization of movement
        edge_template=stretch,
        center=(0, 0, 10), # Start it higher up
        normal=(0, 0, 1)  # XY plane
    )
    

    # Make some nodes of the first sheet static (e.g., top row)
    # And color them differently. Others will be non-static and affected by gravity.
    edge_nodes_sheet1 = sheet1.get_edge_nodes()
    for node in sheet1.nodes:
        if node in edge_nodes_sheet1:
            node.static = True
            node.color = "red"
        else:
            node.color = "green"
            
    
    # Define which nodes to log. Node names are created as f"sheet_{row}_{col}"
    # So, to log nodes like "2_2" and "2_3" (row 2, col 2 and row 2, col 3)
    nodes_to_log_ids = ["sheet_2_2", "sheet_2_3"]

    # Initial render (optional)
    # world.render(pause=True) 

    # Simulate for a few steps with logging
    num_ticks_total = 50
    log_interval = 1 # Log every tick, or change as needed
    render_interval = 5 # Render every 10 ticks, or change as needed

    for i in range(num_ticks_total):
        world.tick(1, nodes_to_log=nodes_to_log_ids)  
        if i % log_interval == 0:
            print(f"Completed Tick {i}")
            # The detailed node logging now happens inside world.tick()
            
        if i > 0 and i % render_interval == 0:
            print(f"Rendering at Tick {i}")
            world.render(pause=True) # Or pause=False, delay=0.1 for quick glances
    
    # Final render
    print("Simulation complete. Final render.")
    world.render(pause=True)


if __name__ == "__main__":
    main() 