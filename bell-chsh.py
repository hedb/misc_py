import random
import csv

'''
        6
    5       1
    4       2
        3
        
          10
      9       1
      
    8           2
    
    7           3
    
      6       4
          5

        
Two cubes are entangled,
cube_a towards Alice's side,
cube_b towards Bob's side.

There are 4 measurement configurations
Pr, Ps, Pt, Pq
Each of them measures the respective properties r, s, t, q

calculating the property i.e. r
r = abs((cube_a-Pr)%6) <= 1
AKA : Is the direction of Alice cube within 1 of the direction of Pr?
 
E(QS + RS + RT − QT ) =? E(QS) + E(RS) + E(RT) − E(QT)

measured_reality = E(QS) + E(RS) + E(RT) − E(QT)

'''



def write_list_of_dicts_to_csv(data, filename):
    if len(data) == 0:
        return

    headers = list(data[0].keys())  # Get the keys from the first dictionary as headers

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()  # Write the headers to the CSV file
        writer.writerows(data)  # Write the data to the CSV file


CUBE_SIDES = 6
# CUBE_SIDES = 10

NUMBER_OF_EXPERIMENTS = 100


def clock_distance(a, b, max_value=10):
    clockwise_distance = (b - a) % max_value
    counter_clockwise_distance = (a - b) % max_value
    return min(clockwise_distance, counter_clockwise_distance)

def collapse_cube(cube, measurement):
    distance = clock_distance(cube % CUBE_SIDES, measurement % CUBE_SIDES, CUBE_SIDES)
    collapse_in_measurement_direction = distance <= ((CUBE_SIDES-2)/4)
    return 1.0 if collapse_in_measurement_direction else -1.0

def test_cube_collapse():
    collapse_cube(1, 2)
    for i in range (1,CUBE_SIDES+1):
        for j in range(1, CUBE_SIDES+1):
            print (f'cube={i}, measurement={j}, collapse={collapse_cube(i, j)}')


def entangle_cubes_3_6():
    entangled_cubes_directions = [CUBE_SIDES, CUBE_SIDES/2]
    rand1 = random.randint(0, 1)
    cube_a = entangled_cubes_directions[rand1]
    cube_b = entangled_cubes_directions[1 - rand1]
    return cube_a, cube_b

def entangle_cubes():
    cube_a = random.randint(1, CUBE_SIDES)
    cube_b = (cube_a + 3) % CUBE_SIDES
    return cube_a, cube_b


def main():
    total_summary = []

    for Pq in range(1, CUBE_SIDES+1):
        for Pr in range(1,CUBE_SIDES+1):
            for Ps in range(1,CUBE_SIDES+1):
                for Pt in range(1,CUBE_SIDES+1):
                    experiment_collector = {'qs':[], 'qt':[], 'rs':[], 'rt':[] }
                    for i in range(NUMBER_OF_EXPERIMENTS):
                        cube_a, cube_b = entangle_cubes()

                        random_var_measured = None
                        random_var_key = ''
                        rand2 = random.randint(0, 1)
                        # Alice decides what to measure
                        if rand2 == 0:
                            random_var_measured = q = collapse_cube(cube_a, Pq)
                            random_var_key = 'q'
                        else:
                            random_var_measured = r = collapse_cube(cube_a, Pr)
                            random_var_key = 'r'

                        rand3 = random.randint(0, 1)
                        # Bob decides what to measure
                        if rand3 == 0:
                            s = collapse_cube(cube_b, Ps)
                            random_var_key += 's'
                            random_var_measured *= s
                        else:
                            t = collapse_cube(cube_b, Pt)
                            random_var_key += 't'
                            random_var_measured *= t

                        experiment_collector[random_var_key].append(random_var_measured)
                    #summary
                    E_qs = sum(experiment_collector['qs'])/len(experiment_collector['qs'])
                    E_qs_desc = f"'{sum(experiment_collector['qs'])}/{len(experiment_collector['qs'])}"
                    E_qt = sum(experiment_collector['qt'])/len(experiment_collector['qt'])
                    E_qt_desc = f"'{sum(experiment_collector['qt'])}/{len(experiment_collector['qt'])}"
                    E_rs = sum(experiment_collector['rs'])/len(experiment_collector['rs'])
                    E_rs_desc = f"'{sum(experiment_collector['rs'])}/{len(experiment_collector['rs'])}"
                    E_rt = sum(experiment_collector['rt'])/len(experiment_collector['rt'])
                    E_rt_desc = f"'{sum(experiment_collector['rt'])}/{len(experiment_collector['rt'])}"

                    measured_reality = E_qs + E_rs + E_rt - E_qt

                    total_summary.append({
                        'Pq': Pq,
                        'Pr': Pr,
                        'Ps': Ps,
                        'Pt': Pt,
                        'E(QS) - desc': E_qs_desc,
                        'E(QS)': E_qs,
                        'E(QT) - desc': E_qt_desc,
                        'E(QT)': E_qt,
                        'E(RS) - desc': E_rs_desc,
                        'E(RS)': E_rs,
                        'E(RT) - desc': E_rt_desc,
                        'E(RT)': E_rt,
                        'E(QS) + E(RS) + E(RT) - E(QT)': measured_reality
                    })

    write_list_of_dicts_to_csv(total_summary, 'bell_inequality.csv')


if __name__ == '__main__':
    main()


'''
Imagine we perform the following experiment, illustrated in Figure 2.4. Charlie pre- pares two particles. 
It doesn’t matter how he prepares the particles, just that he is capable of repeating the experimental procedure
 which he uses. 
Once he has performed the prepa- ration, he sends one particle to Alice, and the second particle to Bob.
Once Alice receives her particle, she performs a measurement on it. 
Imagine that she has available two different measurement apparatuses, so she could choose to do one of 
two different measurements. These measurements are of physical properties which we shall label PQ and PR, 
respectively. Alice doesn’t know in advance which measurement she will choose to perform. Rather, 
when she receives the particle she flips a coin or uses some other random method to decide which measurement to perform.
 We suppose for simplicity that the measurements can each have one of two outcomes, +1 or −1. 
 Suppose Alice’s particle has a value Q for the property PQ. Q is assumed to be an objective 
 property of Alice’s particle, which is merely revealed by the measurement, much as we imagine the position of 
 a tennis ball to be revealed by the particles of light being scattered off it. 
 Similarly, let R denote the value revealed by a measurement of the property PR.
EPR and the Bell inequality 115

Similarly, suppose that Bob is capable of measuring one of two properties, PS or PT , 
once again revealing an objectively existing value S or T for the property, each taking value +1 or −1. 
Bob does not decide beforehand which property he will measure, but waits until he has received the 
particle and then chooses randomly. The timing of the experiment is arranged so that Alice and Bob do their 
measurements at the same time (or, to use the more precise language of relativity, in a causally disconnected manner).
 Therefore, the measurement which Alice performs cannot disturb the result of Bob’s measurement (or vice versa), 
 since physical influences cannot propagate faster than light.
'''
