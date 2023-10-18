import random

poles = [[3,2,1],[],[]]





def calc_valid_steps():
    steps = []
    for i in range(0,3):
        for j in range(0,3):
            if i != j:
                # test step: take from pole i to pole j
                if len(poles[i]) > 0:
                    if len(poles[j]) == 0 or poles[j][-1] > poles[i][-1]:
                        steps.append((i,j))
    return steps

def is_winning_step():
    ret = len(poles[0])==0 and (len(poles[1])==0 or len(poles[2])==0)
    return ret


N = 100000
internal_steps = 1000

didnt_win = 0
win_sum = 0.0

for j in range(N):
    is_won = False
    for i in range(internal_steps):
        # print('current: ', poles)
        steps = calc_valid_steps()
        # print('available: ', steps)
        chosen = steps[random.randint(0,len(steps)-1)]
        # print('choosing ',chosen)
        val = poles[chosen[0]].pop()
        poles[chosen[1]].append(val)
        if is_winning_step():
            win_sum += i
            is_won = True
            break

    if not is_won:
        didnt_win +=1


print('didnt win:', didnt_win)
print('avg win:', win_sum / (N-didnt_win) )
