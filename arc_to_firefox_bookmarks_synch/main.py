import json
import sqlite3
import pandas as pd

import sqlite3
import pandas as pd

from merge_trees import generate_needed_modification_actions, flatten_tree


def save_table_to_csv(db_file, table_name, csv_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Execute a SQL statement to select all rows from the table
    # df = pd.read_sql_query(f"SELECT * FROM {table_name} limit 10", conn)
    df = pd.read_sql_query(f"SELECT * FROM {table_name} where parent = 3", conn)

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)

    # Close the connection
    conn.close()

def create_bookmarks_hierarchy(db_file,root_title):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Execute a SQL statement to select all rows from the table
    df = pd.read_sql_query(f"SELECT bm.id, bm.type, bm.parent, bm.title, url "
                           f"   FROM moz_bookmarks as bm "
                           f"   LEFT JOIN moz_places as p ON bm.fk = p.id", conn)

    # Create a dictionary to hold the nodes
    nodes = {}

    # Add all rows to the dictionary
    for index, row in df.iterrows():
        nodes[row['id']] = {'id': row['id'], 'parent': row['parent'], 'children': [],'title': row['title'],'type': row['type'],'url': row['url']}
        if nodes[row['id']]['title'] == None:
            nodes[row['id']]['title'] = nodes[row['id']]['url']


    # Add each node to its parent's list of children
    for node in nodes.values():
        if node['parent'] is not None and node['parent'] in nodes:
            nodes[node['parent']]['children'].append(node)

    # Find the root nodes (those with no parent)
    root_node = next((node for node in nodes.values() if node['title'] == root_title),None)

    # Close the connection
    conn.close()

    return root_node


def print_tree(node, indent=0):
    # Print the node's title and URL with indentation
    print('  ' * indent + f"{node['title']} : {node['url']}")

    # Recursively print the children of the node
    for child in node['children']:
        print_tree(child, indent + 1)


def collect_nodes(json_data):
    nodes = {}

    def helper(node):
        if 'id' in node:
            if node['id'] in nodes:
                # nodes[node['id']] = { **nodes[node['id']], **node}
                pass
            else:
                nodes[node['id']] = node
            if 'title' not in node or node['title'] == None:
                # print(node['id'])
                if 'data' in node and 'tab' in node['data']:
                    node['title'] = node['data']['tab']['savedTitle']
                    node['url'] = node['data']['tab']['savedURL']
                else:
                    node['title'] = '---- : ' + node['id']



            node['__type'] = "Space" if 'parentID' not in node else "Node"
            if node['__type'] == 'Node' and node['parentID'] == None:
                container = node['data']['itemContainer']['containerType']
                if 'spaceItems' in container:
                    node['parentID'] = container['spaceItems']['_0']


        for key, value in node.items():
            if isinstance(value, dict):
                helper(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        helper(item)

    helper(json_data)
    return nodes


def create_nested_structure(nodes):
    for node in nodes.values():
        parent_id = node.get('parentID')
        if parent_id and parent_id in nodes:
            parent_node = nodes[parent_id]
            if 'children' not in parent_node:
                parent_node['children'] = []
            parent_node['children'].append(node)

    root_nodes = [node for node in nodes.values() if node['__type'] == 'Space']
    return root_nodes

def print_tree(nodes, level=0):
    def safe_get(node,key):
        return node.get(key, '') if node.get(key, '')!=None else ''

    for node in nodes:
        print('     ' * level + safe_get(node,'title') + ' : ' + safe_get(node,'url') )
        print_tree(node.get('children', []), level + 1)

def condense_tree1(tree):
    def helper(node):
        if node['id'] == '2A06C75A-AAE6-41C9-937B-C4FD2385245B' or node['id'] == '4F9523DD-AE8C-4C5B-9CA6-7D22E6F99C29':
            stop = True

        if 'children' in node:
            for child in node['children'].copy():
                if child['title'].startswith('----'):
                    node['children'].remove(child)
                    if 'children' in child:
                        node['children'] += child['children']
                helper(child)

    for node in tree:
        helper(node)

    return tree


def condense_tree(node):
    condensed_children = []

    for child in node.get('children', []):
        if child.get('title', '').startswith('----'):
            condensed_children.extend(child.get('children', []))
        else:
            condense_tree(child)
            condensed_children.append(child)

    node['children'] = condensed_children
    return node



# https://github.com/uuksu/firefox-bookmark-extractor/blob/master/firefox_bookmark_extractor/extractor.py
# hed-bar-nissan@Hed ~ % head ~/Library/Application\ Support/Firefox/Profiles/oa7rg0lm.default-release-4-1658428736890/places.sqlite

FIREFOX_DB_PATH = '/Users/hed-bar-nissan/Library/Application Support/Firefox/Profiles/oa7rg0lm.default-release-4-1658428736890/places.sqlite'

def extract_tree_from_firefox(root_title):
    root_nodes = create_bookmarks_hierarchy(FIREFOX_DB_PATH,root_title)
    # print_tables(file)
    # print_tree(root_nodes[0])
    # save_table_to_csv(file, 'moz_places', '~/moz_places.csv')
    return root_nodes


def extract_tree_from_arc():
    # file_name = '/Users/hed-bar-nissan/StorableSidebar_tmp.json'
    file_name = '/Users/hed-bar-nissan/Library/Application Support/Arc/StorableSidebar.json'
    with open(file_name, 'r') as file:
        json_data = json.load(file)

        nodes = collect_nodes(json_data)
        tree = create_nested_structure(nodes)
        root = {'id': 'root', 'title': '__arc', 'children': tree}
        root = condense_tree(root)
        # print_tree(root['children'])
        return root


def print_actions(actions):
    for action in actions:
        print(action[0], " ::: " ,action[1]['title'], " ::: " ,action[2]," ::: " ,action[3])


def add_bookmark_to_ff(url,title):

    conn = sqlite3.connect(FIREFOX_DB_PATH)
    cur = conn.cursor()

    # Let's say we want to add a bookmark to https://www.example.com. First, we need to add it to the moz_places table.
    cur.execute("INSERT INTO moz_places (url, title) VALUES (?, ?)", (url, title))
    page_id = cur.lastrowid

    # Now we can add the bookmark to the moz_bookmarks table.
    # We'll put it in the Bookmarks Toolbar folder, which has an ID of 3.
    # We'll also set the position to -1, which should make Firefox put it at the end of the toolbar.
    cur.execute("INSERT INTO moz_bookmarks (fk, type, parent, position) VALUES (?, 1, 3, -1)", (page_id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # add_bookmark_to_ff('https://www.example.com','example')
    save_table_to_csv( FIREFOX_DB_PATH , 'moz_bookmarks', '~/moz_bookmarks.csv')



if __name__ == '__main1__':
    new_tree = extract_tree_from_arc()
    new_tree = next(node for node in flatten_tree(new_tree) if node['title'] == '__test_synch')
    # print_tree([new_tree])
    old_tree = extract_tree_from_firefox('__test_synch')
    # print_tree([old_tree])
    actions = generate_needed_modification_actions(old_tree, new_tree)
    print_actions(actions)

    print('done')