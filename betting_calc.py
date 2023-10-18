import random


#rockets-lakers

first_team_win_chances = 65
number_of_wins_needed =  4

first_game_wins_already = 1
second_game_wins_already = 3




series_results = {}
total_experiments = 100000

for i in range(total_experiments):
    results = [first_game_wins_already,second_game_wins_already]
    while results[0]<4 and results[1]<4:
        game_rand = random.randint(1,100)
        if game_rand <= first_team_win_chances:
            results[0]+=1
        else:
            results[1] += 1

    key = '({}:{})'.format(results[0],results[1])
    if key in series_results:
        series_results[key] += 1
    else :
        series_results[key] = 1




for key in sorted(series_results.keys()):
    series_result_chances =  series_results[key]/total_experiments
    money_back_to_break_even_gamble = (1/series_result_chances)-1
    print(key,'\t',series_results[key], '\t',series_result_chances, money_back_to_break_even_gamble)