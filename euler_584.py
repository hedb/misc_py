import random
import time

from dataclasses import dataclass

def birthday_collision_simple(people):
    birthdays = {}
    for p in people:
        if p in birthdays:
            return True
        else:
            birthdays[p] = True
    return False


def birthday_collision1(people,days_in_year,within_X_days_from_each_other,number_of_needed_matches):
    birthdays = [0] * days_in_year
    for p in people:
        birthdays[p] = 1

    match_found = False
    for start_index in range(0,within_X_days_from_each_other):
        if match_found: break
        i = start_index; match_count_till_now = 0; qualifying_matches = []
        while i < days_in_year*2:
            if birthdays[i%days_in_year] == 1:
                match_count_till_now += 1
                qualifying_matches.append(i%days_in_year)
            else :
                match_count_till_now = 0
                qualifying_matches = []
            if match_count_till_now >= number_of_needed_matches:
                match_found = True
                break;
            i+=within_X_days_from_each_other

    # print (match_found,qualifying_matches,people)
    return match_found,qualifying_matches


def birthday_collision(people,days_in_year,within_X_days_from_each_other,number_of_needed_matches):
    match_found = False
    qualifying_matches = []

    birthdays = [0] * days_in_year
    for p in people:
        birthdays[p] += 1

    i = 0; current_sum = 0
    while i < days_in_year + within_X_days_from_each_other + 1:
        running_window_front = i
        running_window_back = i-within_X_days_from_each_other-1
        current_sum += birthdays[running_window_front%days_in_year]
        if running_window_back >= 0:
            current_sum -= birthdays[running_window_back%days_in_year]

        if current_sum >= number_of_needed_matches:
            qualifying_matches = [running_window_back%days_in_year,running_window_front%days_in_year]
            match_found = True
            break
        i+=1


    return match_found,qualifying_matches,current_sum



# print(
#     birthday_collision([2,0,1,2],
#                        days_in_year=11,
#                        within_X_days_from_each_other=2,
#                        number_of_needed_matches=4) \
#     )

assert birthday_collision([],10,1,2)[0] == False
assert birthday_collision([0,1,2],11,2,3)[0] == True
assert birthday_collision([0,1,3],11,2,3)[0] == False
assert birthday_collision([2,0,1,2],11,2,4)[0] == True
assert birthday_collision([10,0,1,2],11,2,4)[0] == False
assert birthday_collision([10,0,1,1],11,2,4)[0] == True
# assert \
#     birthday_collision([9,0,1,2,3,4,5,6,7,8,9],11,2,3)\
#     == (True, [0, 2, 4])
# assert birthday_collision([9,9,1,2,3,9,5,6,7,8,9],11,2,3) == (True, [1,3,5])
# assert birthday_collision([9,9,1,2,3,9,5,9,7,8,9,10],11,2,4) == (True, [8,10,1,3])

# exit()

@dataclass
class ProblemDefinition:
    days_in_a_year: int
    matches_needed: int
    within_X_days_from_each_other: int


def experiment():

    problem = ProblemDefinition(
        days_in_a_year=10,
        matches_needed=2,
        within_X_days_from_each_other=1
    )

    # problem = ProblemDefinition(
    #     days_in_a_year=100,
    #     matches_needed=3,
    #     within_X_days_from_each_other=7
    # )

    N = 100000
    sum = 0

    for i in range(1,N):
        people = []

        tmp_res = None
        while True:
            tmp_res = birthday_collision(people,problem.days_in_a_year,problem.within_X_days_from_each_other,problem.matches_needed)
            if not tmp_res[0]:
                people.append( random.randint(0,problem.days_in_a_year-1) )
            else:
                break

        # print(tmp_res,len(people),people)
        sum += len(people)

    print (sum/N)


# start_time = time.time()
experiment()
# print(time.time()-start_time)

# https://projecteuler.net/problem=584
# https://docs.google.com/spreadsheets/d/11zrNATGqVkPKAX4Kh6DQuFTJ8ZxNyFW25bAFfoG3Lf4/edit#gid=0