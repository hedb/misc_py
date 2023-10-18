import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Modern Data Organization', format='png')

# Define nodes
dot.node('A', 'Incoming Data')
dot.node('B', 'Core Team of Data Engineers\n(Ingesting into DataLake)')
dot.node('C', 'Core Team of Data Engineers\n(Transforming into central DataWarehouse)')
dot.node('D', 'Product Unit')
dot.node('E', 'Team of DataEngineer\n(Producing product dedicated DataWarehouse)')
dot.node('F', 'Team of Data Analysts')

# Define edges (relationships)
dot.edges(['AB', 'BC'])
dot.edge('C', 'D', label='feeds off')
dot.edge('D', 'E')
dot.edge('E', 'F')

# Render and display the graph
dot.render('/Users/hed-bar-nissan/Downloads/data_organization_flow')
dot.view('/Users/hed-bar-nissan/Downloads/data_organization_flow.png')

# Return the path to the generated image for reference
'/mnt/data/data_organization_flow.png'
