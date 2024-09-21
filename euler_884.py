
next_biggest_step_cubed = 8
current_biggest_step_cubed = 1
latest_biggest_step = 1

calc_step_to_0_map = {0: [0,[]]}

def calc_step_to_0(n):
    global latest_biggest_step, current_biggest_step_cubed, next_biggest_step_cubed
    if n == next_biggest_step_cubed:
        latest_biggest_step += 1
        current_biggest_step_cubed = latest_biggest_step ** 3
        next_biggest_step_cubed = (latest_biggest_step + 1) ** 3

    prev_step = calc_step_to_0_map[n - current_biggest_step_cubed]
    val = prev_step[0] + 1
    steps = prev_step[1] + [current_biggest_step_cubed]
    calc_step_to_0_map[n] = [val,steps]
    return val, steps


if __name__ == '__main__':
    s = 0
    for i in range(1, 1000):
        val,steps = calc_step_to_0(i)
        s += val
        print (i, '\t'
                , val, '\t'
                , steps, '\t'
                , s)
