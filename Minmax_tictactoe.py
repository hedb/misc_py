import sys

class NodeType :
    MIN = -1
    MAX = 1

    @staticmethod
    def opposite(type):
        return type*-1



class Node:

    Not_Filled = -99
    RUNNING_ID = 0
    CALC_VALUE_COUNTER = 0

    def __init__(self, type,cells):
        Node.RUNNING_ID +=1
        self.id = Node.RUNNING_ID

        self.type = type
        self.cells = cells
        self.v_is_terminal = Node.Not_Filled
        self.v_next_nodes = Node.Not_Filled
        self.v_utility = Node.Not_Filled

        self.v = -1* sys.maxsize \
            if type == NodeType.MAX \
            else sys.maxsize


    def calc_value(self):
        Node.CALC_VALUE_COUNTER += 1
        print(self)
        if (abs(self.v) == sys.maxsize):
            if (self.is_terminal()) :
                self.v = self.utility()
            else :
                for n in self.next_nodes():
                    if (self.type == NodeType.MAX):
                        self.v = max(self.v,n.calc_value())
                    else :
                        self.v = min(self.v,n.calc_value())
        return self.v


    def state_after_move(self,i):
        ret = list(self.cells);
        ret[i] = self.type
        return ret


    def next_nodes(self):
        if (self.v_next_nodes == Node.Not_Filled):
            self.v_next_nodes = []
            for i in range(len(self.cells)):
                if (self.cells[i] == 0) :
                    self.v_next_nodes.append(Node(NodeType.opposite(self.type),self.state_after_move(i)))
        return self.v_next_nodes



    def is_terminal(self):
        if (self.v_is_terminal == Node.Not_Filled) :
            is_victory = (self.utility() != 0)
            if (is_victory!=True) :
                self_cells = self.cells
                if_full_board = (max(map(lambda x: x==0, self_cells)) == False)
        self.v_is_terminal = (is_victory or if_full_board)
        return self.v_is_terminal



    full_line_combinations_2 = [
        [0,1],[0,2],[0,3],  [1,2],[1,3],    [2,3]
    ]

    full_line_combinations = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    def utility(self):
        if (self.v_utility == Node.Not_Filled):
            self.v_utility = 0
            for comb in self.full_line_combinations:
                if (self.cells[comb[0]]!=0 and
                            #self.cells[comb[0]] == self.cells[comb[1]]):
                            self.cells[comb[0]] == self.cells[comb[1]] and self.cells[comb[1]] == self.cells[comb[2]] ):
                    self.v_utility = self.cells[comb[0]]
                    break
        return self.v_utility


    def __str__(self):
        return str(self.id) + " : " + str(self.cells)

def main():
    n1 = Node(NodeType.MAX,[0,0,0, 0,0,0, 0,0,0])
    print ("calculated game value to be " + str(n1.calc_value()) + " in " + str(Node.CALC_VALUE_COUNTER))


if __name__ == "__main__":
    main()
