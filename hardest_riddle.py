import random
import json


dwarfs, true_ans, false_ans = None, None, None

def initialize():
    global dwarfs, true_ans, false_ans
    dwarf_types = [1, 2, 3]
    random.shuffle(dwarf_types)
    dwarfs =  [{'type': t} for t in dwarf_types]
    true_ans = random.choice(['X', 'Y'])
    false_ans = 'Y' if true_ans == 'X' else 'X'
    return dwarfs, true_ans, false_ans


def answer_as_dwarf(target_dwarf, is_true: bool):
    global dwarfs, true_ans, false_ans

    if (is_true not in [True, False]):
        raise ValueError("is_true must be boolean")

    if target_dwarf['type'] == 1:  # Truth teller
        return true_ans if is_true else false_ans
    elif target_dwarf['type'] == 2:  # Liar
        return false_ans if is_true else true_ans
    else:  # Random answerer
        return random.choice([true_ans, false_ans])


'''
{question_type:1, expected_answer: [X|Y]}  - 
The question is :
If I'd ask the dwarf that is not you and not the random one, if the dwarf that is right to you ( +1 modulo 3 ) is the 
random would he answer expected_answer ?
'''

def question_type_1(dwarf, dwarf_number, expected_answer):
    global dwarfs, true_ans, false_ans
    other_dwarf_im_asking = dwarfs[(dwarf_number + 1)%3]
    # print(dwarfs)
    # print("other dwarf im asking: ", other_dwarf_im_asking)
    if other_dwarf_im_asking['type'] == 3:
        other_dwarf_im_asking = dwarfs[(dwarf_number + 2)%3]

    other_dwarf_im_asking_about = dwarfs[(dwarf_number + 1) % 3]
    return answer_as_dwarf (
        dwarf,
        answer_as_dwarf(other_dwarf_im_asking, other_dwarf_im_asking_about['type'] == 3 ) == 'X'
    )

def ask_dwarf(dwarf_number, question_json):
    global dwarfs, true_ans, false_ans
    question = json.loads(question_json)
    dwarf_number = dwarf_number - 1
    dwarf = dwarfs[dwarf_number]
    expected_answer = question['expected_answer']

    if dwarf["type"] == 3:
        return random.choice([true_ans, false_ans])

    if question['question_type'] == 1:
        return question_type_1(dwarf, dwarf_number, expected_answer)
    if question['question_type'] == 2:
        truth_teller = next(d for d in dwarfs if d['type'] == 1)
        return answer_as_dwarf(dwarf, answer_as_dwarf(truth_teller, True) == expected_answer)
    if question['question_type'] == 3:
        next_dwarf = dwarfs[(dwarf_number +1) % 3]
        return answer_as_dwarf(dwarf, (next_dwarf['type'] == 3) == (expected_answer == true_ans))

def test_ask_dwarf():
    global dwarfs, true_ans, false_ans

    dwarfs, true_ans, false_ans  = initialize()

    dwarfs = [{'type': 1}, {'type': 2}, {'type': 3}]

    question_1 = json.dumps({'question_type': 1, 'expected_answer': 'X'})
    question_2 = json.dumps({'question_type': 2, 'expected_answer': 'X'})
    question_3 = json.dumps({'question_type': 3, 'expected_answer': 'X'})


    '''
    {question_type:1, expected_answer: [X|Y]}  - 
    The question is :
    If 
    I'd ask the dwarf that is not you and not the random one, 
    if the dwarf that is right to you ( +1 modulo 3 ) is the random 
    would he answer expected_answer ?
    
    {question_type:2, expected_answer: [X|Y]}  - 
    The question is :
    If I'd ask the truth sayer if  1==1 would he answer expected_answer ?
    
    {question_type:3, expected_answer: [X|Y]}  - 
    The question is :
    DELETED --- If I'd ask you if the dwarf right to you is random would you answer expected_answer ?
    If I'd ask the truth sayer if the dwarf right to you is random would he answer expected_answer ?
    '''

    # print("config is: ", dwarfs, true_ans, false_ans)

    true_ans = 'X'
    false_ans = 'Y'
    assert ask_dwarf(1, question_1) == true_ans

    true_ans = 'Y'
    false_ans = 'X'
    assert ask_dwarf(1, question_1) == false_ans

    true_ans = 'X'
    false_ans = 'Y'
    assert ask_dwarf(2, question_1) == false_ans
    assert ask_dwarf(3, question_1) in [true_ans, false_ans]

    assert ask_dwarf(1, question_2) == true_ans
    assert ask_dwarf(2, question_2) == false_ans
    assert ask_dwarf(3, question_2) in [true_ans, false_ans]

    assert ask_dwarf(1, question_3) == false_ans
    assert ask_dwarf(2, question_3) == true_ans
    assert ask_dwarf(3, question_3) in [true_ans, false_ans]
    # print("\n\n\n\n\n\n")

# test_ask_dwarf()

def verify_guess(guess,dwarfs):
    print("dwarfs are: ", dwarfs, " true ans is: ", true_ans)
    print("guess is: ", guess)
    for k,v in guess.items():
        val = dwarfs[(k-1)%3]['type'] == v
        assert val
        # print( dwarfs[(k-1)%3]['type'] == v)

    print("\n\n")




def calculate_guess():
    guess = {}
    answer1 = ask_dwarf(1, json.dumps({'question_type': 1, 'expected_answer': 'X'}))
    print("asking #1: answer1 is: ", answer1)
    next_dwarf_to_ask = 2 if answer1 == 'X' else 3
    answer2 = ask_dwarf(next_dwarf_to_ask, json.dumps({'question_type': 2, 'expected_answer': 'X'}))
    print("asking #",next_dwarf_to_ask," answer2 is: ", answer2)
    guess[next_dwarf_to_ask] = 1 if answer2 == 'X' else 2
    answer3 = ask_dwarf(next_dwarf_to_ask, json.dumps({'question_type': 3, 'expected_answer': 'X'}))
    print("asking #", next_dwarf_to_ask, " answer3 is: ", answer3)
    next_dwarf_to_ask_we_decide_on = next_dwarf_to_ask + 1
    if answer3 == 'X' and answer2 == 'X':
        guess[next_dwarf_to_ask_we_decide_on] = 3
    elif answer3 == 'Y' and answer2 == 'X':
        guess[next_dwarf_to_ask_we_decide_on] = 2
    if answer3 == 'X' and answer2 == 'Y':
        guess[next_dwarf_to_ask_we_decide_on] = 1
    elif answer3 == 'Y' and answer2 == 'Y':
        guess[next_dwarf_to_ask_we_decide_on] = 3

    return guess


def test_specific():
    global dwarfs, true_ans, false_ans

    dwarfs =[{'type': 1}, {'type': 2}, {'type': 3}]
    true_ans = 'Y'
    false_ans = 'X'

    # answer1 = ask_dwarf(1, json.dumps({'question_type': 1, 'expected_answer': 'X'}))
    # print("answer1 is: ", answer1)
    # answer1 = ask_dwarf(1, json.dumps({'question_type': 1, 'expected_answer': 'X'}))
    # print("answer1 is: ", answer1)
    # answer1 = ask_dwarf(1, json.dumps({'question_type': 1, 'expected_answer': 'X'}))
    # print("answer1 is: ", answer1)

    guess = calculate_guess()
    verify_guess(guess, dwarfs)


# test_specific()
# exit()


for i in range(0,1000):
    initialize()

    guess = calculate_guess()
    verify_guess(guess,dwarfs)

