from typing import Any, Optional, Union

import numpy as np
import plotly.graph_objects as go
from numpy.typing import NDArray

# Type aliases for better readability
Vector = NDArray[np.float64]  # 3D vector
Coordinate = tuple[float, float, float]
Number = Union[
    float, np.floating[Any]
]  # Accept both Python float and numpy float types


# pylint: disable=R0911
def _format_number(x: float, digits: int = 2) -> str:
    """Format a number for display with specified precision and handle small values.

    Args:
        x: number to format
        digits: number of digits after decimal point

    Returns:
        Formatted string with ellipsis if truncated
    """
    # Handle very small numbers (both positive and negative)
    if abs(x) < 1e-10:
        return "0.0"

    # Convert to float and get initial format with extra precision
    x = float(x)

    # Special case for numbers that round to a different whole number
    test_round = round(x, digits)
    if test_round.is_integer():
        return f"{int(test_round)}.0"

    # Get the decimal string representation
    decimal_str = str(abs(x)).split(".")[1] if "." in str(abs(x)) else ""

    # Handle small numbers that need leading zeros
    if abs(x) < 1:
        leading_zeros = len(decimal_str) - len(decimal_str.lstrip("0"))

        # If we have more leading zeros than our precision, show them
        if leading_zeros >= digits:
            return f"{'-' if x < 0 else ''}0.{'0' * digits}..."

        # If we have exactly the precision in significant digits
        if len(decimal_str) == digits:
            return f"{'-' if x < 0 else ''}0.{decimal_str}"

        # If we have more digits than precision
        if len(decimal_str) > digits:
            return f"{'-' if x < 0 else ''}0.{decimal_str[:digits]}..."

    # Format with specified precision
    formatted = f"{abs(x):.{digits}f}"
    whole, _, decimal = formatted.partition(".")

    # If it's a whole number or we want no decimals
    if decimal == "0" * digits or digits == 0:
        return f"{'-' if x < 0 else ''}{whole}.0"

    # Check if there are more digits after what we're showing
    has_more = len(decimal_str) > digits

    # Build the final string
    sign = "-" if x < 0 else ""
    if has_more:
        return f"{sign}{whole}.{decimal}..."
    return f"{sign}{whole}.{decimal}"


def _format_vector_debug(v: Vector) -> str:
    """Format vector for debug/repr with full precision."""
    clean_v = [0.0 if abs(float(x)) < 1e-10 else float(x) for x in v]
    return str(tuple(clean_v))


def _format_vector_display(v: Vector, digits: int = 2) -> str:
    """Format vector for display with specified precision."""
    return str(tuple(_format_number(float(x), digits) for x in v))


class Node:
    def __init__(
        self, coordinates: Coordinate, *, static: bool = False, name: str = ""
    ) -> None:
        World.get_instance().nodes.append(self)
        self.coordinates = np.array(coordinates, dtype=float)
        self.static = static
        self.forces: list[Force] = []
        self.edges: list[Edge] = []
        self.name = name
        self.color: Optional[str] = None  # Added color attribute

    def __repr__(self) -> str:
        return (
            f"Node:{self.name} ({_format_vector_debug(self.coordinates)}, "
            + f"static={self.static})"
        )

    def __str__(self) -> str:
        return (
            f"Node:{self.name} ({_format_vector_display(self.coordinates)}, "
            + f"static={self.static})"
        )

    def calculate_net_force(self) -> "Force":
        """Calculate the net force acting on this node."""
        # Start with zero force
        net_force = Force(direction=(0, 0, 0), strength=0)

        # Return zero force if static
        if self.static:
            return net_force

        # Add all direct forces
        for force in self.forces:
            net_force.add(force)

        # Add edge forces
        for edge in self.edges:
            net_force += Force(
                direction=edge.direction_from(self),
                strength=edge.calculate_force_magnitude(),
            )

        return net_force

    def apply_force(self, force: "Force", dt: float) -> None:
        if not self.static:
            # Simple Euler integration using NumPy
            force_vector = force.direction * force.strength
            self.coordinates += force_vector * dt


class StretchFunction:
    def __init__(self, func_type: str, rest_length: float, unit_inc: float) -> None:
        self.func_type = func_type
        self.rest_length = rest_length
        self.unit_inc = unit_inc

    def calculate_force_magnitude(self, length: float) -> float:
        if self.func_type == "linear":
            return (length - self.rest_length) * self.unit_inc

        raise ValueError(f"Unknown stretch function type: {self.func_type}")


class Edge:
    def __init__(self, node1: Node, node2: Node, *, stretch: StretchFunction) -> None:
        self.node1 = node1
        self.node2 = node2
        self.stretch = stretch

        node1.edges.append(self)
        node2.edges.append(self)

    def __repr__(self) -> str:
        return f"Edge({self.node1!r} -> {self.node2!r}, stretch={self.stretch!r})"

    def __str__(self) -> str:
        force = self.calculate_force_magnitude()
        return (
            f"Edge({str(self.node1)} -> {str(self.node2)}, "
            + f"force={_format_number(force)})"
        )

    def calculate_force_magnitude(self) -> float:
        length = np.linalg.norm(self.node1.coordinates - self.node2.coordinates)
        force_magnitude = self.stretch.calculate_force_magnitude(length)
        return force_magnitude

    def direction_from(self, node: Node) -> Vector:
        ret = None
        if node == self.node1:
            ret = self.node2.coordinates - self.node1.coordinates
        elif node == self.node2:
            ret = self.node1.coordinates - self.node2.coordinates
        else:
            raise ValueError(f"Node {node} is not part of this edge")

        return ret / np.linalg.norm(ret)


class Force:
    def __init__(self, *, direction: Coordinate, strength: Number = 1.0) -> None:
        self.direction = self._normalize_direction(np.array(direction, dtype=float))
        self.strength = float(strength)  # Convert to Python float for consistency

    def _normalize_direction(self, direction: Vector) -> Vector:
        """Normalize a direction vector to unit length."""
        norm = np.linalg.norm(direction)
        if norm > 0:
            return direction / norm
        return np.zeros(3)

    def __repr__(self) -> str:
        return (
            f"Force({_format_vector_debug(self.direction)}, strength={self.strength})"
        )

    def __str__(self) -> str:
        return (
            f"Force({_format_vector_display(self.direction)}, "
            + f"strength={_format_number(self.strength)})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare two forces for equality."""
        if not isinstance(other, (Force, tuple, list, np.ndarray)):
            return NotImplemented

        if isinstance(other, Force):
            return np.allclose(self.direction, other.direction) and np.isclose(
                self.strength, other.strength
            )

        # If comparing with a vector-like object (tuple/list/array)
        other_array = np.asarray(other)
        if other_array.shape != (3,):
            return False

        # Compare with the effective force vector (direction * strength)
        return np.allclose(self.direction * self.strength, other_array)

    def __array__(self) -> Vector:
        """Convert force to its effective vector representation."""
        return self.direction * self.strength

    def __add__(self, other: "Force") -> "Force":
        """Support for the + operator. Returns a new Force object."""
        if other is None:
            raise ValueError("other is None")

        # NumPy vector addition
        v1 = self.direction * self.strength
        v2 = other.direction * other.strength

        result_vector = v1 + v2
        magnitude = np.linalg.norm(result_vector)

        # Update the force
        if magnitude > 0:
            result = Force(direction=result_vector / magnitude, strength=magnitude)
            return result

        return Force(direction=(0, 0, 0), strength=0)

    def add(self, other: "Force") -> None:
        """Add another force vector to this one in-place."""
        if other is None:
            raise ValueError("other is None")

        # Use __add__ implementation and apply results to self
        result = self + other
        self.direction = result.direction
        self.strength = result.strength

    def copy(self) -> "Force":
        """Create a copy of this force."""
        return Force(direction=tuple(self.direction), strength=self.strength)


class World:
    the_world: Optional["World"] = None

    def __init__(self) -> None:
        self.nodes: list[Node] = []

    @classmethod
    def get_instance(cls) -> "World":
        if cls.the_world is None:
            cls.the_world = World()
        return cls.the_world

    def render(self) -> None:
        if not self.nodes:
            return

        # Extract coordinates for all nodes
        x, y, z = zip(*[node.coordinates for node in self.nodes])

        # Determine node colors
        node_colors = [node.color if node.color else "blue" for node in self.nodes]

        # Create scatter plot for nodes
        nodes_trace = go.Scatter3d(
            x=x, y=y, z=z,
            mode="markers",
            marker=dict(
                size=8,
                color=node_colors,  # Use individual node colors
            ),
            name="Nodes",
            text=[f"Node {i}" for i in range(len(self.nodes))],
            hoverinfo="text"
        )

        # Create lines for edges
        edge_x, edge_y, edge_z = [], [], []
        for node in self.nodes:
            for edge in node.edges:
                # Only process each edge once
                if edge.node1 == node:
                    edge_x.extend([edge.node1.coordinates[0], edge.node2.coordinates[0], None])
                    edge_y.extend([edge.node1.coordinates[1], edge.node2.coordinates[1], None])
                    edge_z.extend([edge.node1.coordinates[2], edge.node2.coordinates[2], None])

        edges_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode="lines",
            line=dict(color="gray", width=2),
            name="Edges",
            hoverinfo="none"
        )

        # Create the figure
        fig = go.Figure(data=[nodes_trace, edges_trace])
        
        # Update layout for better visualization
        fig.update_layout(
            showlegend=True,
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
                aspectmode="data"
            ),
            width=800,
            height=800,
            title="3D World Visualization"
        )

        fig.show()

    def tick(self, n: int) -> None:
        for i in range(n):
            for node in self.nodes:
                if not node.static:
                    net_force = node.calculate_net_force()
                    # print(f"Tick {i}: {str(node)}, Net force: {str(net_force)}")
                    node.apply_force(net_force, dt=1)
