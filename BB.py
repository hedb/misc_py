import random

import itertools


class Feeder:
    def __init__(self):
        self.tape = {0:0}
        self.head = 0  # position of the tape head
        self.min_pos = 0
        self.max_pos = 0

    def read(self):
        """Read the symbol at the current tape head position."""

        if self.head not in self.tape:
            self.tape[self.head] = 0

        return self.tape[self.head]

    def write(self, symbol):
        """Write a symbol at the current tape head position."""
        self.tape[self.head] = symbol

    def move(self, direction):
        """Move the tape head in the given direction."""
        if direction == 'R':
            self.head += 1
            self.max_pos = max(self.max_pos,self.head)
        elif direction == 'L':
            self.head -= 1
            self.min_pos = min(self.min_pos,self.head)

    def __str__(self):
        return f'Tape: pos: {self.head}, val: {self.read()}'


class TuringMachine:

    states = ['A', 'B', 'H']  # including halt state 'H'
    symbols = [0, 1]
    directions = ['L', 'R']

    def __init__(self, transitions,state,halt_):
        self.transitions = transitions
        self.state = state
        self.prev_state = None
        self.halt_ = halt_

    def __str__(self):
        return 'TuringMachine:\n' + \
            ('\n'.join(f" {key}: {value}" for key, value in self.transitions.items()))

    def read(self, symbol):
        next_state, write, move = self.transitions[(self.state, symbol)]
        self.prev_state = self.state
        self.state = next_state
        return (write, move) if next_state != self.halt_ else (None, None)

    def __eq__(self, other):
        return all(k in other.transitions and self.transitions[k] == other.transitions[k] for k in self.transitions.keys() if k[0] != self.halt_)


    @classmethod
    def random_machine(cls):
        """Randomly generate a Turing machine."""
        transitions = {}
        halting_transition = (random.choice(cls.states[:-1])  , random.choice(cls.symbols))
        for state in cls.states[:-1]:
            for symbol in cls.symbols:
                next_state = random.choice(cls.states[:-1])
                if (state,symbol) == halting_transition:
                    next_state = cls.states[-1]
                write = random.choice(cls.symbols)
                move = random.choice(cls.directions)
                transitions[(state, symbol)] = (next_state, write, move)
        return cls(transitions,cls.states[0],cls.states[-1])

    @classmethod
    def all_machines(cls):
        """Generator to iterate over all possible Turing machines."""
        states_without_the_halt = cls.states[:-1]
        keys = list(itertools.product(states_without_the_halt, cls.symbols))
        values = list(itertools.product(states_without_the_halt, cls.symbols, cls.directions))
        for transitions in itertools.product(values, repeat=len(keys)):
            trans_dict = {k: v for k, v in zip(keys, transitions)}
            for k in trans_dict.keys():
                tm = cls(trans_dict.copy(), cls.states[0], cls.states[-1])
                tm.transitions[k] = (cls.states[-1],) + tm.transitions[k][1:]
                yield tm



def print_state(feeder, TM):
    feeder.read()
    # Convert the tape dict to a sorted list of values
    tape_list = [value for key, value in sorted(feeder.tape.items())]

    tape_zero_position = abs(min(feeder.tape.keys()))

    # Construct the tape string with '|' separator
    tape_str = ''.join(map(str, tape_list))
    tape_str = tape_str[:tape_zero_position] + '|' + tape_str[tape_zero_position:]

    # Construct the head position string with '*' indicator
    head_str = ' ' * ((feeder.head-feeder.min_pos) + (1 if feeder.head>=0 else 0) ) + '*'  # +1 to account for '|'

    # Get the current transition
    current_value = feeder.read()
    transition = str((TM.state, current_value)) + ' => '+ str(TM.transitions.get((TM.state, current_value), None))

    # Print the notation
    my_log(head_str)
    my_log(tape_str)
    my_log(f"Transition: {transition}")




def run_experiment(tm = None):
    tm = tm or TuringMachine.random_machine()
    if not is_valid_machine(tm):
        raise ValueError(f"Invalid Turing machine: {tm}")
    feeder = Feeder()

    my_log(  str(tm) + '\n' )

    MAX_STEPS = 100
    past_edge_moves_left = set()
    past_edge_moves_right = set()
    is_halt = False

    for i in range(MAX_STEPS+1):

        # my_log(f'Step:{i} ({feeder.head+1}, {symbol}, {tm.prev_state}) => ({move}, {tm.state})')
        my_log(f'\nStep:{i+1}')
        print_state(feeder, tm)
        symbol = feeder.read()

        if feeder.head == feeder.min_pos:
            if (tm.state,symbol) in past_edge_moves_left:
                break
            else:
                past_edge_moves_left.add((tm.state,symbol))
        if feeder.head == feeder.max_pos:
            if (tm.state,symbol) in past_edge_moves_right:
                break
            else:
                past_edge_moves_right.add((tm.state,symbol))


        write, move = tm.read(symbol)

        if write is None:
            is_halt = True
            break
        feeder.write(write)
        feeder.move(move)

    return (is_halt,i+2, tm)


def my_log(s):
    # print(s)
    pass

def run_specific_tm():
    interesting_transitions = \
        {('A', 0): ('B', 1, 'R'), ('A', 1): ('H', 1, 'L'), ('B', 0): ('C', 1, 'L'), ('B', 1): ('C', 1, 'R'),
         ('C', 0): ('B', 0, 'R'), ('C', 1): ('B', 1, 'L'), ('H', 0): ('C', 1, 'L'), ('H', 1): ('B', 1, 'L')}

    interesting_transitions = {
        ('A', 0): ('B', 1, 'R'),  # On state A, reading 0: write 1, move right, change to state B
        ('A', 1): ('H', 1, 'N'),  # On state A, reading 1: write 1, do not move, halt
        ('B', 0): ('A', 1, 'L'),  # On state B, reading 0: write 1, move left, change to state A
        ('B', 1): ('B', 1, 'R')  # On state B, reading 1: write 1, move right, stay in state B
    }

    interesting_transitions = {('A', 0): ('B', 1, 'L'), ('A', 1): ('A', 0, 'R'), ('B', 0): ('B', 1, 'R'), ('B', 1): ('A', 1, 'L'), ('H', 0): ('H', 1, 'R'), ('H', 1): ('H', 1, 'R')}

    interesting_transitions = {
        ('A', 0): ('B', 1, 'R'),  # On state A, reading 0: write 1, move right, change to state B
        ('A', 1): ('B', 1, 'L'),  # On state A, reading 1: write 1, do not move, halt
        ('B', 0): ('A', 1, 'L'),  # On state B, reading 0: write 1, move left, change to state A
        ('B', 1): ('H', 1, 'R')  # On state B, reading 1: write 1, move right, stay in state B
    }

    interesting_transitions =\
    {('A', 0): ('C', 0, 'R'), ('A', 1): ('A', 0, 'L'), ('B', 0): ('C', 1, 'L'), ('B', 1): ('C', 1, 'R'),
     ('C', 0): ('B', 1, 'R'), ('C', 1): ('B', 1, 'L'), ('H', 0): ('H', 1, 'L'), ('H', 1): ('B', 0, 'R')}

    interesting_transitions = \
        {('A', 0): ('B', 1, 'R'), ('A', 1): ('B', 1, 'R'), ('B', 0): ('A', 1, 'L'), ('B', 1): ('B', 0, 'L'),
         ('H', 0): ('B', 0, 'R'), ('H', 1): ('A', 1, 'R')}

    tm = TuringMachine.random_machine()
    tm.transitions = interesting_transitions

    is_halt,steps, tm =run_experiment(tm)
    print(f'is_halt:{is_halt}, steps:{steps}, tm:{tm.transitions}')


def run_N_experiments():
    interesting_tm = []
    N = 100000
    stats = {}  # Dictionary to hold the statistics

    halted_exp = 0
    for i in range(N):
        is_halt, step_no, tm = run_experiment()

        key = (is_halt, step_no + 1)
        stats[key] = stats.get(key, 0) + 1

        # 2: 6
        # 3: 21
        if step_no > 7:
            interesting_tm.append( (is_halt,step_no,tm) )
        halted_exp += is_halt
        # print(f'{is_halt}\t{step_no + 1}')

    print(f'\t\tExperiment halted in {halted_exp} out of {N} experiments.')
    print_stats(stats, N)

    for is_halt,step_no,tm in interesting_tm:
        print(f'\t\t{is_halt}\t{step_no + 1}\t{tm.transitions}')


def print_stats(stats, total):
    """
    Print the accumulated stats as a table.

    :param stats: The statistics dictionary.
    :param total: The total number of experiments.
    """
    print("Is Halted, Steps to Identify, COUNTA of Is Halted")
    for (is_halt, steps), count in sorted(stats.items(), key=lambda x: (x[0][0], x[0][1])):
        print(f"{is_halt}, {steps}, {count}")


def iterate_all_possible_machines():
    N = 0
    stats = {}  # Dictionary to hold the statistics

    specific_machine = TuringMachine.random_machine()
    specific_machine.transitions = \
        {
            ('A', 0): ('B', 1, 'R'), ('A', 1): ('B', 1, 'R'),
            ('B', 0): ('A', 1, 'L'), ('B', 1): ('B', 0, 'L'),
            ('H', 0): ('B', 0, 'R'), ('H', 1): ('A', 1, 'R')}


    for tm in TuringMachine.all_machines():
        if tm==specific_machine:
            print (f'found specific machine {tm}')
        N += 1
        is_halt, step_no, tm = run_experiment(tm)

        # Update the stats
        key = (is_halt, step_no + 1)
        stats[key] = stats.get(key, 0) + 1

        # Print update every 100 steps
        if N % 100000 == 0:
            print(f"After {N} experiments:")
            print_stats(stats, N)
            print(f'Sample machine:{tm}\n\n')

    # Print the final statistics
    print("Final statistics:")
    print_stats(stats, N)


def is_valid_machine(tm):
    """
    Verify if the given Turing Machine is valid.

    :param tm: An instance of the TuringMachine class.
    :return: True if the TM is valid, False otherwise.
    """
    # Check if all state and symbol pairs have a defined transition

    states_without_halt = tm.states[:-1]
    found_halt = False
    for state in states_without_halt:
        for symbol in tm.symbols:
            if (state, symbol) not in tm.transitions:
                return False
            else:
                if tm.transitions[(state, symbol)][0] == tm.states[-1]:
                    found_halt = True

    if not found_halt:
        return False

    # Check if each transition is valid
    for (state, symbol), (next_state, write, move) in tm.transitions.items():
        # Check if next_state is a valid state
        if next_state not in tm.states:
            return False

        # Check if write is a valid symbol
        if write not in tm.symbols:
            return False

        # Check if move is a valid direction
        if move not in tm.directions:
            return False

    return True

def test_all_machines_generator():
    """
    Iterate over the first 100 Turing machines and validate each one.
    """
    count = 0
    for tm in TuringMachine.all_machines():
        if (tm.transitions[('A', 0)] == ('B', 1, 'R') and tm.transitions[('A', 1)] == ('B', 1, 'R')):
                # tm.transitions[('B', 0)] == ('A', 1, 'L') and tm.transitions[('B', 1)] == ('B', 0, 'L') and
                # tm.transitions[('H', 0)] == ('B', 0, 'R') and tm.transitions[('H', 1)] == ('A', 1, 'R')):
            print(f'found specific machine {tm}')

        count += 1
        if count >= 1000000:  # stop after checking 100 machines
            break
        if not is_valid_machine(tm):
            print(f'machine {str(tm)} is not valid')
            exit(1)

    print(f'All machines are valid, tested {count} machines')

def test_TM():
    tm = TuringMachine.random_machine()
    tm1 = TuringMachine.random_machine()
    assert tm != tm1
    tm1.transitions = tm.transitions
    assert tm == tm1


if __name__ == '__main__':
    # test_TM()
    # run_specific_tm()
    # run_N_experiments()
    # test_all_machines_generator()
    iterate_all_possible_machines()