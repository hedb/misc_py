import csv
from copy import deepcopy


has_letter = {"a":set(), "b":set(), "c":set(), "d":set(), "e":set(), "f":set(), "g":set(), "h":set(), "i":set(), "j":set(), "k":set(), "l":set(), "m":set(), "n":set(), "o":set(), "p":set(), "q":set(), "r":set(), "s":set(), "t":set(), "u":set(), "v":set(), "w":set(), "x":set(), "y":set(), "z":set()}
doesnt_have_letter = {}

has_letter_at_a_position = [deepcopy(has_letter),deepcopy(has_letter),deepcopy(has_letter),deepcopy(has_letter),deepcopy(has_letter)]
doesnt_have_letter_at_a_position = [{},{},{},{},{}]

candidates = []
candidates_ids = set()

with open('/Users/hed-bar-nissan/Downloads/5ngrams.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # csv_reader = [ ['abcde'] , ['abcdd'], ['abccc'], ['bbccc'] ]
    id = 0
    for row in csv_reader:
        candidates_ids.add(id)
        candidates.append(row[0])
        for pos,c in enumerate(row[0]):
            has_letter[c].add(id)
            has_letter_at_a_position[pos][c].add(id)
        id += 1

for c in has_letter.keys():
    doesnt_have_letter[c] = candidates_ids.difference(has_letter[c])

for pos,letters_at_pos in enumerate(has_letter_at_a_position):
    for c in letters_at_pos.keys():
        doesnt_have_letter_at_a_position[pos][c] = candidates_ids.difference(has_letter_at_a_position[pos][c])


def diffentiated_candidates(words):
    dim = -1
    match_scores = [0] * len(candidates)
    letters = set()
    pos_letters = [set(),set(),set(),set(),set()]
    for word in words:
        for pos, c in enumerate(word):
            letters.add(c)
            pos_letters[pos].add(c)

    for c in letters:
        dim += 1
        for id in doesnt_have_letter[c]:
            match_scores[id] += pow(2,dim)

    for pos,letters_in_pos in enumerate(pos_letters):
        for c in letters_in_pos:
            dim += 1
            for id in doesnt_have_letter_at_a_position[pos][c]:
                match_scores[id] += pow(2,dim)


    return match_scores



ret = diffentiated_candidates([ candidates[0], candidates[1], candidates[2] ,candidates[3] ])


cardinality = {}

for score in ret:
    if score not in cardinality:
        cardinality[score] = 0
    cardinality[score] += 1

l = sorted(cardinality.items(), key=lambda item: item[1])

print(l[0],l[1],'...',l[-2],l[-1])


