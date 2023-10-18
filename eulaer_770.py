
# https://projecteuler.net/problem=770
# https://docs.google.com/spreadsheets/d/1sPgF7OhCkW4mOka4eKiAX3rPD0LEGHbeWLntx5RVR84/edit#gid=0




def best_strategy_assured_gain(take_count,give_count):
    print('best_strategy_assured_gain({},{}):'.format(take_count,give_count))
    if (take_count == 0):
        return pow(2,give_count)
    elif (give_count == 0):
        return 1
    else:
        r = best_strategy_assured_gain(take_count-1,give_count)
        t = best_strategy_assured_gain(take_count,give_count-1)
        x = (r-t) / (r+t)
        return (1-x)*r


print (best_strategy_assured_gain(1,1))
print (best_strategy_assured_gain(1,2))
