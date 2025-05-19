from world_objects import World, StretchFunction
from sheet import Sheet

def main():
    # Reset the world
    World.the_world = None
    world = World.get_instance()
    
    # Create a stretch function for the edges
    stretch = StretchFunction(func_type="linear", rest_length=1.0, unit_inc=1.0)
    
    # Create a sheet in the XY plane
    sheet = Sheet(
        hex_count=(6, 6),  # 6×6 hexagons
        edge_template=stretch,
        center=(0, 0, 0),
        normal=(0, 0, 1)  # XY plane
    )
    
    # Color the nodes of the first sheet
    edge_nodes_sheet1 = sheet.get_edge_nodes()
    for node in sheet.nodes:
        if node in edge_nodes_sheet1:
            node.color = "red"  # Edge nodes in red
        else:
            node.color = "green" # Interior nodes in green
    
    # Create another sheet at an angle
    sheet2 = Sheet(
        hex_count=(4, 4),
        edge_template=stretch,
        center=(5, 0, 5),
        normal=(1, 0, 1)  # Tilted 45 degrees around Y axis
    )
    
    # Render the world
    world.render()

if __name__ == "__main__":
    main() 