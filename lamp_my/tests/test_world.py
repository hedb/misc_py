import numpy as np

from world_objects import Edge, Force, Node, StretchFunction, World


def test_node_and_force() -> None:
    A = Node((0, 0, 0), static=False)
    f1 = Force(direction=(0, 1, 0), strength=0.5)
    A.forces.append(f1)

    world = World.get_instance()
    world.tick(3)

    assert np.allclose(A.coordinates, (0, 1.5, 0))

    f2 = Force(direction=(0, 0, 1), strength=0.5)
    A.forces.append(f2)

    net_force = A.calculate_net_force()
    assert np.allclose(
        net_force, Force(direction=(0, 0.5**0.5, 0.5**0.5), strength=0.5**0.5)
    ), f"Net force: {net_force}"


def test_3_nodes_and_middle_force() -> None:
    A = Node((0, 0, 0), static=True, name="A")
    B = Node((1, 0, 0), static=False, name="B")
    C = Node((2, 0, 0), static=True, name="C")

    stretch = StretchFunction(func_type="linear", rest_length=1.0, unit_inc=1.0)
    Edge(A, B, stretch=stretch)
    Edge(B, C, stretch=stretch)

    # Create force with direction and strength
    f1 = Force(direction=(0, 1, 0), strength=0.5)
    B.forces.append(f1)

    world = World.get_instance()
    world.tick(10)
    assert np.allclose(B.coordinates, (1, 0.93166583, 0)), f"B.coordinates: {B.coordinates}"

    world.render()


if __name__ == "__main__":
    test_3_nodes_and_middle_force()
