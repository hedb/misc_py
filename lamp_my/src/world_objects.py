from typing import Optional

import numpy as np

# Type aliases for better readability
Vector = np.ndarray  # 3D vector
Coordinate = tuple[float, float, float]


class Node:
    def __init__(self, coordinates: Coordinate, *, static: bool = False) -> None:
        World.get_instance().nodes.append(self)
        self.coordinates = np.array(coordinates, dtype=float)
        self.static = static
        self.forces: list[Force] = []
        self.edges: list[Edge] = []

    def __str__(self) -> str:
        return f"Node({tuple(self.coordinates)})"

    def calculate_net_force(self) -> "Force":
        net_force = Force(direction=(0, 0, 0), strength=0)
        if self.static:
            return net_force

        for force in self.forces:
            net_force.add(force)

        for edge in self.edges:  # type: Edge
            net_force += Force(
                direction=(self.coordinates - edge.node2.coordinates),
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

    def __str__(self) -> str:
        return f"Edge({self.node1}, {self.node2})"

    def calculate_force_magnitude(self) -> float:
        length = np.linalg.norm(self.node1.coordinates - self.node2.coordinates)
        force_magnitude = self.stretch.calculate_force_magnitude(length)
        return force_magnitude


class Force:
    def __init__(self, *, direction: Coordinate, strength: float = 1.0) -> None:
        self.direction = self._normalize_direction(np.array(direction, dtype=float))
        self.strength = strength

    def _normalize_direction(self, direction: Vector) -> Vector:
        """Normalize a direction vector to unit length."""
        norm = np.linalg.norm(direction)
        if norm > 0:
            return direction / norm
        return np.zeros(3)

    def __str__(self) -> str:
        return f"Force({tuple(self.direction)}, {self.strength})"

    def __add__(self, other: "Force") -> "Force":
        """Support for the + operator. Returns a new Force object."""
        if other is None:
            raise ValueError("other is None")

        result = Force(direction=(0, 0, 0), strength=0)

        # NumPy vector addition
        v1 = self.direction * self.strength
        v2 = other.direction * other.strength

        result_vector = v1 + v2
        magnitude = np.linalg.norm(result_vector)

        # Update the force
        if magnitude > 0:
            result.direction = result_vector / magnitude
            result.strength = magnitude

        return result

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

    def tick(self, n: int) -> None:
        for _ in range(n):
            for node in self.nodes:
                if not node.static:
                    net_force = node.calculate_net_force()
                    node.apply_force(net_force, dt=1)
