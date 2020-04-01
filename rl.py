import random
import math
import timeit

'''''
SIGMA = 1.0
MAX_DEPTH = 4
STANDARD = 2
MAX_RANGE = 5000
LAMBDA = 0.1
'''''

'''
#krylov
SIGMA = 1.0
MAX_DEPTH = 4
STANDARD = 2
MAX_RANGE = 5000
LAMBDA = 0.1
'''


'''
#krinsky
SIGMA = 1.0
MAX_DEPTH = 6
STANDARD = 2
MAX_RANGE = 5000
LAMBDA = 0.1
'''




#LR1 && testlin
SIGMA = 1.0
MAX_DEPTH = 6
STANDARD = 2
MAX_RANGE = 5000
LAMBDA = 0.1 



def get_permutation():
    array = [1, 2, 3, 4, 5, 6]
    random.shuffle(array)
    return array


def strength(position, q):
    return 0.8 * q[position] + 0.4 * math.ceil(q[position] / 2) + random.gauss(0, math.pow(SIGMA, 2))


def environment(i, q):
    j = strength(i - 1, q)
    return STANDARD > j


def update_s(s):
    if s % MAX_DEPTH != 1:
        s -= 1
    return s


def pick_random_state():
    return random.randint(1, 6)


def norm_list(raw):
    norm = [i/sum(raw) for i in raw]
    return norm


def add_lists(first, second):
    newList = [x + y for x, y in zip(first, second)]
    return newList


def make_choice(s):
    if 1 <= s <= MAX_DEPTH:
        return 1
    if MAX_DEPTH + 1 <= s <= 2 * MAX_DEPTH:
        return 2
    if (2 * MAX_DEPTH) + 1 <= s <= 3 * MAX_DEPTH:
        return 3
    if (3 * MAX_DEPTH) + 1 <= s <= 4 * MAX_DEPTH:
        return 4
    if (4 * MAX_DEPTH) + 1 <= s <= 5 * MAX_DEPTH:
        return 5
    if (5 * MAX_DEPTH) + 1 <= s <= 6 * MAX_DEPTH:
        return 6
    return 0


def give_penalty(s):
    if s % MAX_DEPTH != 0:
        return s + 1
    elif s == MAX_DEPTH:
        return 2 * MAX_DEPTH
    elif s == MAX_DEPTH * 2:
        return 3 * MAX_DEPTH
    elif s == MAX_DEPTH * 3:
        return 4 * MAX_DEPTH
    elif s == MAX_DEPTH * 4:
        return 5 * MAX_DEPTH
    elif s == MAX_DEPTH * 5:
        return 6 * MAX_DEPTH
    elif s == MAX_DEPTH * 6:
        return MAX_DEPTH


q = get_permutation()


def testlin(q):
    # Set up variables
    total_result = [0] * 6
    for i in range(0, 100):
        level = 0  # can be any number
        count = 0
        s = pick_random_state()
        score = [0] * 6
        for converge in range(0, MAX_RANGE):
            reward = environment(level, q)  # environment judging
            # automata starts
            # update s
            if reward:
                if s % MAX_DEPTH != 1:
                    s -= 1
            else:  # giving penalty
                s = give_penalty(s)
            # make choice
            level = make_choice(s)

            count += 1
            if count > MAX_RANGE-1000:
                score[level - 1] += 1

        result = norm_list(score)
        total_result = add_lists(result, total_result)
    print(total_result)


def krinsky(q):
    # Set up variables
    total_result = [0] * 6
    for i in range(0, 100):
        level = 0  # can be any number
        count = 0
        s = pick_random_state()
        score = [0] * 6
        for converge in range(0, MAX_RANGE):
            reward = environment(level, q)  # environment judging
            # automata starts
            # update s
            if reward:
                if 1 <= s <= MAX_DEPTH:
                    s = 1
                elif MAX_DEPTH + 1 <= s <= MAX_DEPTH * 2:
                    s = MAX_DEPTH + 1
                elif 2 * MAX_DEPTH + 1 <= s <= MAX_DEPTH * 3:
                    s = 2 * MAX_DEPTH + 1
                elif 3 * MAX_DEPTH + 1 <= s <= MAX_DEPTH * 4:
                    s = 3 * MAX_DEPTH + 1
                elif 4 * MAX_DEPTH + 1 <= s <= MAX_DEPTH * 5:
                    s = 4 * MAX_DEPTH + 1
                elif 5 * MAX_DEPTH + 1 <= s <= MAX_DEPTH * 6:
                    s = 5 * MAX_DEPTH + 1

            else:  # giving penalty
                s = give_penalty(s)

            # make choice
            level = make_choice(s)
            count += 1
            if count > MAX_RANGE-1000:
                score[level - 1] += 1

        result = norm_list(score)
        total_result = add_lists(result, total_result)
    print(total_result)


def krylov(q):
    # Set up variables
    total_result = [0] * 6
    for i in range(0, 100):
        level = 0  # can be any number
        count = 0
        s = pick_random_state()
        score = [0] * 6
        for converge in range(0, MAX_RANGE):
            reward = environment(level, q)  # environment judging
            # automata starts
            # update s
            if reward:
                if s % MAX_DEPTH != 1:
                    s -= 1
            else:  # giving penalty
                if random.random() < 0.5:
                    if s % MAX_DEPTH != 1:
                        s -= 1
                else: # penalty
                    s = give_penalty(s)
            # make choice
            level = make_choice(s)

            count += 1
            if count > MAX_RANGE-1000:
                score[level - 1] += 1

        result = norm_list(score)
        total_result = add_lists(result, total_result)
    print(total_result)


def pick_action(action_prob):
    ran_numb = random.random()
    for i in range(0, 6):
        if ran_numb - action_prob[i] < 0:
            return i
        ran_numb -= action_prob[i]
    return 5;


def update_action_prob(level, action_prob):
    sum = 0
    for j in range(0, 6):
        if j != level:
            action_prob[j] *= (1 - LAMBDA)
            sum += action_prob[j]
    action_prob[level] = 1 - sum
    return action_prob

def lr1(q):
    # Set up variables
    total_result = [0] * 6
    for i in range(0, 100):
        level = 0  # can be any number
        count = 0
        score = [0] * 6
        action_prob = [1/6] * 6
        for converge in range(0, MAX_RANGE):

            level = pick_action(action_prob)
            reward = environment(level, q)  # environment judging

            if reward:  # reward! change action_prob!
                action_prob = update_action_prob(level,action_prob)
            count += 1
            if count > MAX_RANGE-1000:
                score[level - 1] += 1

        result = norm_list(score)
        total_result = add_lists(result, total_result)
    print(total_result)


start = timeit.default_timer()

#testlin(q)
#krinsky(q)
#krylov(q)
lr1(q)
print(q)

stop = timeit.default_timer()

print('Time: ', stop - start)


