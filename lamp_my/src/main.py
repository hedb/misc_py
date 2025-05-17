from world_objects import Edge, Force, Node, StretchFunction, World


def main() -> None:
    print("Hello from lamp-my!")


if __name__ == "__main__":
    main()

    A = Node((0, 0, 0), static=True)
    B = Node((1, 0, 0), static=False)
    C = Node((2, 0, 0), static=True)

    stretch = StretchFunction(func_type="linear", rest_length=1.0, unit_inc=1.0)
    edge1 = Edge(A, B, stretch=stretch)
    edge2 = Edge(B, C, stretch=stretch)

    # Create force with direction and strength
    f1 = Force(direction=(0, 1, 0), strength=0.5)
    B.forces.append(f1)

    # Print initial positions
    print("Initial positions:")
    print(f"Node A: {tuple(A.coordinates)}")
    print(f"Node B: {tuple(B.coordinates)}")
    print(f"Node C: {tuple(C.coordinates)}")

    # Run simulation
    world = World.get_instance()
    world.tick(3)

    # Print final positions
    print("\nFinal positions after 3 ticks:")
    print(f"Node A: {tuple(A.coordinates)}")  # Should not move (static)
    print(f"Node B: {tuple(B.coordinates)}")  # Should move up in Y direction
    print(f"Node C: {tuple(C.coordinates)}")  # Should not move (static)
