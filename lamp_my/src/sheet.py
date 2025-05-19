import numpy as np
from typing import Optional, Tuple

from world_objects import Node, Edge, StretchFunction, World

class Sheet:
    def __init__(
        self,
        hex_count: Tuple[int, int],
        edge_template: StretchFunction,
        center: Tuple[float, float, float] = (0, 0, 0),
        normal: Tuple[float, float, float] = (0, 0, 1),
    ) -> None:
        """Create a hexagonally-tiled sheet of nodes.
        
        Args:
            hex_count: Approximate width and height in hexagons (cols, rows)
            edge_template: Template for creating edges between nodes
            center: Center point of the sheet
            normal: Normal vector to the plane
        """
        self.hex_count = hex_count
        self.edge_template = edge_template
        self.center = np.array(center, dtype=float)
        self.normal = self._normalize_vector(np.array(normal, dtype=float))
        
        # Calculate spacing based on the rest length
        self.spacing = edge_template.rest_length
        
        # Generate the nodes and edges
        self.nodes = []
        self._create_nodes_and_edges()
    
    def _normalize_vector(self, vector: np.ndarray) -> np.ndarray:
        """Normalize a vector to unit length."""
        norm = np.linalg.norm(vector)
        if norm > 0:
            return vector / norm
        return vector
    
    def _create_basis_vectors(self) -> Tuple[np.ndarray, np.ndarray]:
        """Create basis vectors for the plane."""
        # Find two orthogonal vectors in the plane
        if np.allclose(self.normal, [0, 0, 1]):
            # If normal is z-axis, use x and y axes as basis
            basis_x = np.array([1, 0, 0])
            basis_y = np.array([0, 1, 0])
        else:
            # Find a vector not parallel to normal
            if not np.allclose(self.normal, [1, 0, 0]):
                temp = np.array([1, 0, 0])
            else:
                temp = np.array([0, 1, 0])
            
            # First basis vector is perpendicular to normal
            basis_x = np.cross(self.normal, temp)
            basis_x = self._normalize_vector(basis_x)
            
            # Second basis vector is perpendicular to both normal and basis_x
            basis_y = np.cross(self.normal, basis_x)
            basis_y = self._normalize_vector(basis_y)
        
        return basis_x, basis_y
    
    def _create_nodes_and_edges(self) -> None:
        """Create nodes in a hexagonal pattern and connect them with edges."""
        cols, rows = self.hex_count
        basis_x, basis_y = self._create_basis_vectors()
        
        # Constants for hexagonal grid
        hex_width = self.spacing
        hex_height = np.sqrt(3) * self.spacing / 2
        
        # Create a mapping to store nodes by their grid coordinates
        grid_to_node = {}
        
        # Create nodes
        for row in range(rows):
            for col in range(cols):
                # In hexagonal grid, even rows are offset
                offset = hex_width / 2 if row % 2 == 1 else 0
                
                # Calculate position in 2D grid
                x_pos = col * hex_width + offset
                y_pos = row * hex_height
                
                # Adjust to center the grid
                x_pos -= (cols * hex_width) / 2
                y_pos -= (rows * hex_height) / 2
                
                # Project onto the 3D plane
                position = self.center + (x_pos * basis_x) + (y_pos * basis_y)
                
                # Create the node
                node = Node(
                    coordinates=tuple(position),
                    name=f"sheet_{row}_{col}"
                )
                self.nodes.append(node)
                grid_to_node[(row, col)] = node
        
        # Connect nodes with edges
        for row in range(rows):
            for col in range(cols):
                # Define the 6 neighbor positions in grid coordinates
                if row % 2 == 0:
                    # Even rows
                    neighbors = [
                        (row, col+1),     # right
                        (row+1, col),     # bottom right
                        (row+1, col-1),   # bottom left
                        (row, col-1),     # left
                        (row-1, col-1),   # top left
                        (row-1, col),     # top right
                    ]
                else:
                    # Odd rows
                    neighbors = [
                        (row, col+1),     # right
                        (row+1, col+1),   # bottom right
                        (row+1, col),     # bottom left
                        (row, col-1),     # left
                        (row-1, col),     # top left
                        (row-1, col+1),   # top right
                    ]
                
                # Get the current node
                current_node = grid_to_node.get((row, col))
                if not current_node:
                    continue
                
                # Connect to each valid neighbor
                for neighbor_row, neighbor_col in neighbors:
                    # Skip if neighbor is outside grid
                    if (
                        neighbor_row < 0 or
                        neighbor_row >= rows or
                        neighbor_col < 0 or
                        neighbor_col >= cols
                    ):
                        continue
                    
                    # Get the neighbor node
                    neighbor_node = grid_to_node.get((neighbor_row, neighbor_col))
                    if not neighbor_node:
                        continue
                    
                    # Check if edge already exists
                    edge_exists = False
                    for edge in current_node.edges:
                        if (edge.node1 == neighbor_node or edge.node2 == neighbor_node):
                            edge_exists = True
                            break
                    
                    # Create edge if it doesn't exist
                    if not edge_exists:
                        Edge(
                            node1=current_node,
                            node2=neighbor_node,
                            stretch=self.edge_template
                        ) 