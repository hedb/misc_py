
import unittest



def generate_needed_modification_actions(old, new):

    # Validate and fix the tree structur
    validate_and_fix_tree_structure(old)
    validate_and_fix_tree_structure(new)

    #verify same root node
    if old['title'] != new['title']:
        raise ValueError("Root node title mismatch")


    def get_node_external_identifier(node):
        if 'url' in node and node['url'] is not None:
            return node['url']
        else:
            return node['title']

    old_nodes_by_external_id = {get_node_external_identifier(node): node for node in flatten_tree(old)}
    new_nodes_by_external_id = {get_node_external_identifier(node): node for node in flatten_tree(new)}

    # old_nodes_by_internal_id = {node['id']: node for node in flatten_tree(old)}
    new_nodes_by_internal_id = {node['id']: node for node in flatten_tree(new)}

    actions1 = []

    for external_id, new_node in new_nodes_by_external_id.items():
        if external_id not in old_nodes_by_external_id:
            # Node is in new tree but not in old tree: add it
            parent_node = new_nodes_by_internal_id[new_node.get('parent_id')]
            parent_url = parent_node.get('url') if parent_node else None
            parent_title = parent_node.get('title') if parent_node else None
            actions1.append({"type":'add', "node":new_node, "parent_url":parent_url, "parent_title":parent_title})  # Include parent_url and parent_title
        else:
            # Node is in both trees: check for changes
            old_node = old_nodes_by_external_id[external_id]
            if old_node['title'] != new_node['title']:
                actions1.append({"type":'change', "identifying_url": old_node['url'], 'new_title':new_node['title']})

    for external_id, old_node in old_nodes_by_external_id.items():
        if external_id not in new_nodes_by_external_id:
            # Node is in old tree but not in new tree: remove it
            actions1.append({'type':'remove', 'external_id':external_id})

    # Generate 'connect' actions for all nodes in new tree
    # for identifier, new_node in new_nodes.items():
    #     for child in new_node['children']:
    #         child_identifier = child.get('url', child['title'])
    #         actions.append(('connect', child_identifier, identifier))

    return actions1


def flatten_tree(node):
    """Flatten a hierarchical tree into a list of nodes."""
    nodes = [node]
    if 'children' in node:
        for child in node['children']:
            nodes.extend(flatten_tree(child))
    return nodes

def validate_and_fix_tree_structure(node, parent=None):
    # If the node has a 'parent_id' attribute, check if it's consistent with the actual parent

    if 'title' not in node and 'url' not in node:
        raise ValueError(f"Node {node['id']} has no title or URL")
    if 'title' not in node or 'url' not in node:
        if 'title' not in node:
            node['title'] = node.get('url')
        else:
            node['url'] = node.get('title')
    if 'id' not in node:
        node['id'] = node.get('url')

    if 'parent_id' in node:
        if node['parent_id'] != parent['id']:
            raise ValueError(f"Node {node['id']} has inconsistent parent attribute")
    else:
        # If the node doesn't have a 'parent_id' attribute but it does have a parent, add the attribute
        if parent is not None:
            node['parent_id'] = parent['id']

    # Check if the node is included in its parent's 'children' list, and if not, add it
    if parent is not None and not any(child == node for child in parent['children']):
        parent['children'].append(node)

    # Recursively check and fix all child nodes
    if 'children' in node:
        for child in node['children']:
            validate_and_fix_tree_structure(child, node)

def perform_actions(tree, actions):
    # Create a dictionary to look up nodes by URL or title

    def get_node_external_identifier(node):
        if 'url' in node and node['url'] is not None:
            return node['url']
        else:
            return node['title']

    nodes = { get_node_external_identifier(node) : node for node in flatten_tree(tree)}

    for action1 in actions:
        if action1['type'] == 'add':
            # Add a node
            node = action1['node']
            parent_url = action1['parent_url']  # Parent URL
            parent_title = action1['parent_title']  # Parent title

            if parent_url or parent_title:
                parent_id = parent_url or parent_title
                parent_node = nodes.get(parent_id)
                if parent_node:
                    parent_node['children'].append(node)
                else:
                    raise KeyError(f"No parent node found with identifier: {parent_id}")
            else:
                # If no parent is specified, add it to the root of the tree
                tree['children'].append(node)

            nodes[node.get('url', node['title'])] = node

        elif action1['type'] == 'remove':
            # Remove a node
            identifier = action1['external_id']
            node = nodes[identifier]
            parent_node = nodes.get(node.get('parent_id'))
            if parent_node:
                parent_node['children'].remove(node)
            del nodes[identifier]

        elif action1['type'] == 'change':
            # Change a node's title
            identifier = action1['identifying_url']
            new_title = action1['new_title']
            nodes[identifier]['title'] = new_title

        else:
            raise ValueError(f"Unknown action type: {action1['type']}")
        # elif action1['type'] == 'connect':
        #     # Connect two nodes
        #     child_identifier = action[1]
        #     parent_identifier = action[2]
        #     child_node = nodes[child_identifier]
        #     parent_node = nodes[parent_identifier]
        #     parent_node['children'].append(child_node)

    return tree



class TestModifications(unittest.TestCase):
    def test_modifications(self):
        # Define the old and new trees
        old = {'url': 'A', 'children': [{'url': 'B', 'children': []}]}
        new = {'url': 'A', 'children': [{'url': 'B', 'children': []}]}
        actions = generate_needed_modification_actions(old, new)
        assert actions == []

        old = {'url': 'A', 'children': [{'url': 'B', 'children': []}]}
        new = {'url': 'A', 'children': [{'url': 'B', 'children': []},{'url': 'C', 'children': []}]}
        actions = generate_needed_modification_actions(old, new)
        assert len(actions)==1 and actions[0]['type'] == 'add'
        modified_old = perform_actions(old, actions)
        assert modified_old == new

        old = {'url': 'A', 'children': [{'url': 'B', 'children': []}]}
        new = {'url': 'A', 'children': [ {'url': 'C', 'children': []}] }
        actions = generate_needed_modification_actions(old, new)
        modified_old = perform_actions(old, actions)
        assert modified_old == new

        old = { 'url': 'A', 'children':
            [ {'url': 'D', 'children': [{'url': 'B', 'children': []}]} ]
        }
        new = {'url': 'A', 'children': [{'url': 'C', 'children': []}]}
        actions = generate_needed_modification_actions(old, new)
        modified_old = perform_actions(old, actions)
        assert modified_old == new

if __name__ == '__main__':
    unittest.main()
