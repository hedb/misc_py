from Minmax_tictactoe import Node
from Minmax_tictactoe import NodeType




def main2():

    n1 = Node(NodeType.MIN,[0,0,0,0])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MIN,[0,0,0,1])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MIN,[0,0,-1,1])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MIN,[0,1,-1,1])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MIN,[1,-1,1,0])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MIN,[0,-1,-1,1])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MIN,[1,2,3,4])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )



def main3():

    n1 = Node(NodeType.MAX,[0,0,0, 0,0,0, 0,0,0])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MAX,[-1, 1, -1, 1, 1, -1, 1, 0, -1])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MAX,[0,0,0, 0,0,0, 1,1,1])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MAX,[0,0,0, 1,1,1, 0,0,0])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )

    n1 = Node(NodeType.MAX,[1,0,0, 1,0,0, 1,0,0])
    print(str(n1) + " is_terminal = " + str(n1.is_terminal()) )


if __name__ == "__main__":
    main3()
