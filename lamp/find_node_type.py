import hou
import sys

def find_node_type_by_description(search_description):
    """
    Attempts to create a node based on a user-friendly description
    and prints its internal type name and description.
    """
    print(f"--- Searching for node with description similar to: '{search_description}' ---")

    obj_context = hou.node("/obj")
    if obj_context is None:
        print("ERROR: /obj context not found!", file=sys.stderr)
        return

    # Create a temporary geo node
    temp_geo = None
    try:
        temp_geo = obj_context.createNode("geo", "temp_geo_for_type_find")
        if temp_geo is None:
            print("ERROR: Could not create temporary geo node.", file=sys.stderr)
            return

        print(f"Looking for SOPs inside {temp_geo.path()}...")

        # Method 1: Attempt to create directly if the description is close to a type name
        # This is less reliable for user descriptions.
        # created_node = temp_geo.createNode(search_description, "test_node")

        # Method 2: Iterate through all SOP node types and compare descriptions
        # This is more robust for finding by user-friendly names.
        found_node_info = []
        for category in hou.nodeTypeCategories().values():
            if category.name() == "Sop": # Surface OPerators
                for node_type_name, node_type_obj in category.nodeTypes().items():
                    description = node_type_obj.description().lower()
                    if search_description.lower() in description:
                        found_node_info.append({
                            "internal_name": node_type_name,
                            "description": node_type_obj.description()
                        })

        if not found_node_info:
            print(f"No SOP node type found with '{search_description}' in its description.")
            # Try to create a generic 'group' node as a fallback to see its type
            print("Attempting to create a generic 'group' node (groupcreate) as a fallback example:")
            try:
                generic_group_node = temp_geo.createNode("group", "generic_group_test") # 'group' often maps to 'groupcreate'
                if generic_group_node:
                    print(f"  Fallback Generic 'group' node successfully created:")
                    print(f"    Internal Type Name: {generic_group_node.type().name()}")
                    print(f"    User Description:   {generic_group_node.type().description()}")
                else:
                    print("  Failed to create fallback generic 'group' node.")
            except hou.OperationFailed as e:
                print(f"  Failed to create fallback generic 'group' node: {e}")

        else:
            print(f"\nFound potential matches for '{search_description}':")
            for info in found_node_info:
                print(f"  ------------------------------")
                print(f"  User Description:   {info['description']}")
                print(f"  Internal Type Name: {info['internal_name']}")
                # Optionally, try to create it to be absolutely sure
                try:
                    test_node = temp_geo.createNode(info['internal_name'], "test_creation")
                    if test_node:
                        print(f"    Successfully created with internal name: {info['internal_name']}")
                        test_node.destroy() # Clean up
                    else:
                        print(f"    Failed to create using internal name: {info['internal_name']}")
                except hou.OperationFailed:
                    print(f"    Failed to create using internal name (hou.OperationFailed): {info['internal_name']}")


    except hou.OperationFailed as e:
        print(f"ERROR: Operation failed - {e}", file=sys.stderr)
        print("This might mean the initial search description was too vague or the node doesn't exist as expected.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    finally:
        if temp_geo:
            temp_geo.destroy() # Clean up the temporary geo node
        print("--- Search finished ---")

if __name__ == "__main__":
    # --- What are you looking for? ---
    # Try different descriptions if the first one doesn't work.
    search_term = "Group Range"
    # search_term = "Group by Range"
    # search_term = "Range Group"
    # search_term = "Group" # Will list many, including the basic one.

    if len(sys.argv) > 1:
        search_term = " ".join(sys.argv[1:]) # Allow passing search term as command line argument

    find_node_type_by_description(search_term)