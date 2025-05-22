from typing import Any, Optional, Union

import numpy as np
import plotly.graph_objects as go
from numpy.typing import NDArray
import time # Added import for time.sleep

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
        self, coordinates: Coordinate, *, static: bool = False, name: str = "", mass: float = 1.0
    ) -> None:
        # Ensure world is initialized before creating nodes
        world = World.get_instance() # This will now raise error if not initialized
        world.nodes.append(self)
        
        self.coordinates = np.array(coordinates, dtype=float)
        self.velocity: Vector = np.zeros(3, dtype=float) # Added velocity
        self.static = static
        self.forces: list[Force] = []
        self.edges: list[Edge] = []
        self.name = name
        self.color: Optional[str] = None
        self.mass: float = mass

    def __repr__(self) -> str:
        return (
            f"Node:{self.name} ({_format_vector_debug(self.coordinates)}, "
            + f"v={_format_vector_debug(self.velocity)}, " # Added velocity
            + f"static={self.static}, mass={self.mass})"
        )

    def __str__(self) -> str:
        return (
            f"Node:{self.name} ({_format_vector_display(self.coordinates)}, "
            + f"v={_format_vector_display(self.velocity)}, " # Added velocity
            + f"static={self.static}, mass={_format_number(self.mass)})"
        )

    def calculate_net_force(self) -> "Force":
        """Calculate the net force acting on this node, including gravity."""
        # Start with zero force
        net_force = Force(direction=(0, 0, 0), strength=0)

        # Return zero force if static (gravity and other forces don't cause movement)
        if self.static:
            return net_force

        # Apply gravity if it's defined in the world
        world = World.get_instance()
        if world.gravity_effect is not None and self.mass > 0:
            # Create a specific force instance for this node's gravity
            # F_gravity = m * g_acceleration_force_object
            node_gravity_force = Force(
                direction=world.gravity_effect.direction,
                strength=world.gravity_effect.strength * self.mass
            )
            net_force.add(node_gravity_force)

        # Add all direct forces explicitly applied to the node
        for force in self.forces:
            net_force.add(force)

        # Add edge forces
        for edge in self.edges:
            net_force += Force( # Using __add__ which creates a new Force object
                direction=edge.direction_from(self),
                strength=edge.calculate_force_magnitude(),
            )
        return net_force

    def apply_force(self, force: "Force", dt: float) -> None:
        if not self.static:
            if self.mass <= 0:
                return
            
            force_vector = force.direction * force.strength
            acceleration = force_vector / self.mass
            
            self.velocity += acceleration * dt
            # Get damping factor from the world instance
            world = World.get_instance()
            self.velocity *= world.damping_factor 
            self.coordinates += self.velocity * dt


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

    def __init__(self, gravity_accel: Optional[Coordinate] = None, damping_factor: float = 1.0) -> None:
        if World.the_world is not None:
            raise RuntimeError(
                "World instance already exists. Use World.reset() or World.get_instance()."
            )
        
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.gravity_effect: Optional[Force] = None
        self.damping_factor: float = damping_factor # Added damping_factor

        if gravity_accel is not None:
            # Gravity is an acceleration. To make it a force, we'd multiply by mass,
            # but here we store it as a 'template' force with strength 1,
            # and mass is applied in Node.calculate_net_force.
            # The direction is the accel direction, strength is its magnitude.
            # This might be confusing; a better name might be gravity_acceleration_template.
            # For now, gravity_effect acts as a normalized direction vector for gravity,
            # and its strength component is the magnitude of g.
            g_strength = np.linalg.norm(np.array(gravity_accel))
            if g_strength > 0:
                self.gravity_effect = Force(direction=gravity_accel, strength=g_strength)
            else:
                self.gravity_effect = None # No gravity if (0,0,0)
        else:
            self.gravity_effect = None
        
        World.the_world = self

    @classmethod
    def init_world(cls, *, gravity_accel: Optional[Coordinate] = None, damping_factor: float = 1.0) -> "World":
        if cls.the_world is not None:
            print("Warning: World instance already exists. Resetting and re-initializing.")
            cls.reset(gravity_accel=gravity_accel, damping_factor=damping_factor)
        else:
            cls.the_world = World(gravity_accel=gravity_accel, damping_factor=damping_factor)
        return cls.the_world

    @classmethod
    def get_instance(cls) -> "World":
        if cls.the_world is None:
            # Default initialization if get_instance is called before init_world
            # This ensures a world always exists but might not be configured as expected.
            # Consider if this is the desired behavior or if it should raise an error.
            # For now, let's initialize with defaults to prevent crashes.
            print("Warning: World.get_instance() called before init_world. Initializing with defaults.")
            cls.the_world = World(damping_factor=1.0) # Default damping
        return cls.the_world

    @classmethod
    def reset(cls, *, gravity_accel: Optional[Coordinate] = None, damping_factor: float = 1.0) -> "World":
        cls.the_world = None
        return cls.init_world(gravity_accel=gravity_accel, damping_factor=damping_factor)

    def render(self, *, pause: bool = True, delay: float = 0.0) -> None: # Modified signature
        if not self.nodes:
            return

        # Extract coordinates for all nodes
        x, y, z = zip(*[node.coordinates for node in self.nodes])

        # Determine node colors
        node_colors = [node.color if node.color else "blue" for node in self.nodes]

        # Generate hover text for nodes
        hover_texts = []
        for i, node in enumerate(self.nodes):
            text_to_display = ""
            if node.name: # Use node.name if available
                if node.name.startswith("sheet_"):
                    # Extract coordinate part like "2_2" from "sheet_2_2"
                    parts = node.name.split("_", 1) # Split only on the first underscore
                    if len(parts) > 1:
                        text_to_display = parts[1]
                    else:
                        text_to_display = node.name # Fallback to full name if format is unexpected
                else:
                    text_to_display = node.name # Use the full custom name
            else:
                text_to_display = f"Node {i}" # Fallback if name is empty
            hover_texts.append(text_to_display)

        # Create scatter plot for nodes
        nodes_trace = go.Scatter3d(
            x=x, y=y, z=z,
            mode="markers",
            marker=dict(
                size=8,
                color=node_colors,  # Use individual node colors
            ),
            name="Nodes",
            text=hover_texts, # Use custom hover texts
            hoverinfo="text" # Ensure only the text is shown on hover
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

        if pause:
            # Add an input prompt to block execution until Enter is pressed
            try:
                input("Plot window displayed. Press Enter in the console to continue and close the script...")
            except EOFError:
                # Handle cases where input might not be available (e.g., some non-interactive environments)
                print("Plot window displayed. Continuing as no interactive input is available.")
        elif delay > 0:
            time.sleep(delay)
        # If not pausing and no delay, script continues immediately after fig.show()

    def tick(self, n: int, *, nodes_to_log: Optional[list[str]] = None) -> None:
        if nodes_to_log is None:
            nodes_to_log = [] # Default to empty list if not provided

        # Prepare a set for faster lookups if we are logging specific node names
        # This also handles the "sheet_X_Y" -> "X_Y" conversion for logging
        log_name_set = set()
        for name_to_log in nodes_to_log:
            if name_to_log.startswith("sheet_"):
                parts = name_to_log.split("_", 1)
                if len(parts) > 1:
                    log_name_set.add(parts[1])
                else:
                    log_name_set.add(name_to_log) # Log full name if format unexpected
            else:
                log_name_set.add(name_to_log)

        for tick_num in range(n): # Renamed loop variable from i to tick_num
            # First, calculate all net forces based on the current state
            forces_to_apply: list[tuple[Node, Force]] = []
            for node in self.nodes:
                if not node.static:
                    net_force = node.calculate_net_force()
                    forces_to_apply.append((node, net_force))

                    # Logging logic
                    current_node_log_name = ""
                    if node.name:
                        if node.name.startswith("sheet_"):
                            parts = node.name.split("_", 1)
                            if len(parts) > 1:
                                current_node_log_name = parts[1]
                            else:
                                current_node_log_name = node.name
                        else:
                            current_node_log_name = node.name
                    
                    if current_node_log_name in log_name_set:
                        print(f"Tick {tick_num}: Node {node.name} (LogID: {current_node_log_name}) - "
                              f"Pos: {_format_vector_display(node.coordinates)}, "
                              f"Vel: {_format_vector_display(node.velocity)}, "
                              f"NetForce: {str(net_force)}")
            
            # Then, apply all calculated forces to update positions
            for node, net_force in forces_to_apply:
                node.apply_force(net_force, dt=1) # dt=1 is a placeholder, should be configurable
