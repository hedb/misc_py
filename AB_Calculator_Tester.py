from AB_Calculator import calc
import numpy as np


if __name__ == "__main__":


    exp_length_in_days = 28
    a_rate = .02
    ab_diff = 0.01
    daily_N = 30000.0
    std_perc = .02
    run_summary = {'didnt finish':0, 'B didnt lose' :0, 'B lost':0, 'days finished':0, 'total_days':0}

    result = b_lost = days_to_finish = NA = NB = SXA = SXB = 0
    for i in range(exp_length_in_days):
        NA_daily = np.random.normal(daily_N,daily_N*std_perc)
        NB_daily = np.random.normal(daily_N, daily_N*std_perc)
        SXA_daily = np.random.normal(daily_N*a_rate, daily_N*a_rate*std_perc)
        SXB_daily = np.random.normal(daily_N * (a_rate * (1+ab_diff)), daily_N * (a_rate * (1+ab_diff)) * std_perc)

        NA += NA_daily
        NB += NB_daily
        SXA += SXA_daily
        SXB += SXB_daily

        test_input = {
            'A':{'N':NA, 'SX':SXA, 'SX2':SXA},
            'B':{'N':NB, 'SX':SXB, 'SX2':SXB},
            'tails':1, 'alpha':.05, 'direction':1, 'MDE':.03
        }
        result = calc(test_input)
        if (result['test_completion'] == 1 or (result['lift'] + result['ci'])<0 ):
            days_to_finish = i+1
            break




    if (days_to_finish == 0):
        # test didn't finish within 40 days
        run_summary['didnt finish'] += 1
    else:
        run_summary['days finished'] +=1
        run_summary['total_days'] += days_to_finish
        if (  (result['lift'] + result['ci'])<0 ):
            run_summary['B lost'] += 1
        else :
            run_summary['B didnt lose'] += 1

    print(run_summary)
