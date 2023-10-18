
import array
import random
import json

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import string

def init_tsp():
    # gr*.json contains the distance map in list of list style in JSON format
    # Optimal solutions are : gr17 = 2085, gr24 = 1272, gr120 = 6942
    with open("./gr17.json", "r") as tsp_data:
        tsp = json.load(tsp_data)

    distance_map = tsp["DistanceMatrix"]
    IND_SIZE = tsp["TourSize"]

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    context = {'toolbox':toolbox}

    # Attribute generator
    toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)

    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evalTSP(individual):
        distance = distance_map[individual[-1]][individual[0]]
        for gene1, gene2 in zip(individual[0:-1], individual[1:]):
            distance += distance_map[gene1][gene2]
        return distance,

    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evalTSP)
    return context

def run_tsp():
    random.seed(169)
    context = init_tsp()
    toolbox = context['toolbox']

    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 40, stats=stats,
                        halloffame=hof)

    return pop, stats, hof

queries = []
orig_table = []

def init():
    if len(queries) == 0:
        with open('./query_expressions.csv', "r") as queries_file:
            for q in queries_file:
                queries.append(q)
        with open('./table.csv', "r") as table_file:
            for t in table_file:
                orig_table.append(t)


def calc_indexes(order1, order2, t):

    first_index = [None,None]
    second_index = [None,None]
    for i, v in enumerate(order1):
        if v in t:
            if first_index[0] == None: first_index[0] = i;
            first_index[1] = i;

    for i, v in enumerate(order1):
        if v in t:
            if second_index[0] == None: second_index[0] = i;
            second_index[1] = i;

    return first_index[0], second_index[0]

def calc_bq_scan_cost(order1,order2):
    ordered_table = []
    for t in orig_table:
        first_index, second_index = calc_indexes(order1, order2, t)
        ordered_table.append({'v':t, 'i1':first_index, 'i2':second_index})

    def according_to_i1i2(elem):
        return elem["i1"]*1000+elem["i2"] # NO MORE THAN 1000 VALUES IN ORDER
    ordered_table.sort(key=according_to_i1i2)

    indexes = {}
    prev_ind1 = None
    for i,t in enumerate(ordered_table):
        if prev_ind1 != t['i1']:
            indexes[t['i1']] = i
            prev_ind1 = t['i1']

    def get_first_indexes(requested_ind):
        ret = len(indexes)
        for i in range(requested_ind,len(indexes)):
            if i in indexes:
                ret = i; break
        return ret


    cost = 0
    for q in queries:
        first_index, second_index = calc_indexes(order1, order2, q)
        cost += len(orig_table) - get_first_indexes(first_index)

    return cost




default_order1 = list(string.ascii_lowercase[:26])
default_order2 = list(reversed(default_order1))

def run_bq_opt():

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    context = {'toolbox':toolbox}

    toolbox.register("indices", random.sample, range(len(default_order1)), len(default_order1))

    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)


    def eval_bq_cost(individual):
        new_partition_order = []
        for i in individual:
            new_partition_order.append(default_order1[i])
        return calc_bq_scan_cost(new_partition_order,default_order2),

    toolbox.register("evaluate", eval_bq_cost)

    toolbox = context['toolbox']

    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 40, stats=stats,
                        halloffame=hof)

    return pop, stats, hof

if __name__ == "__main__":
    init()
    random.seed(169)

    # default_cost = len(orig_table) * len(queries)
    # improved_cost = calc_bq_scan_cost(default_order1,default_order2)
    # print(improved_cost / default_cost)
    res = run_bq_opt()
    print(res)