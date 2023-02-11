import numpy as np
import random
from tabulate import tabulate


def fill_shift(shift: int, hours: int) -> np.array:
    """the function generates random shifts within the total number of people available. There are two shift types
    full shift = total working hours and half_shift = half of total working hours
    :param shift: the max number of agents available
    :param hours: the timetable when it is possible to start shift
    :return: 2D numpy array with numbers of agents assigned to the certain time slot
    """
    counter = shift
    my_arr = np.zeros((hours, hours))
    for j in range(hours):
        start = random.randint(0, hours - 1)
        shift_dur = random.choice([hours // 2, hours])
        shift_adjusted = hours - 1 - start
        shift_factual = start + shift_dur if shift_dur <= shift_adjusted else start + shift_adjusted + 1
        var = random.randint(0, counter)
        counter -= var
        for i in range(start, shift_factual):
            my_arr[j, i] = var
    return my_arr


def fitness(hours: int, my_arr: np.array) -> np.array:
    """The function compares the ideal shift to one of randomly generated and returns sum of absolute values
    of all differences for each time slot
    :param hours: TODO change to ideal match
    :param my_arr: the schedule created by 'fill_shift' function
    :return: absolute error
    """
    ideal_array = np.ones((hours, hours))
    diff_array = abs(my_arr - ideal_array)
    result = np.sum(diff_array)
    return result


def generate_population(length: int, shift: int, hours: int, selection: int) -> tuple:
    """This function generates tuple of size length where the first element is population of shifts, second element is
     based on element's rank the list of weighted probabilities of being selected and third element is the list of
     selected shifts of size of selection
    :param length: size of population
    :param shift: the max number of agents available
    :param hours: the timetable when it is possible to start shift
    :return: tuple(population list, weighted probabilities of being selected list, selected populations list)
    """
    population = [fill_shift(shift, hours) for i in range(length)]
    population = sorted(population, key=lambda x: fitness(hours, x), reverse=True)
    d = sum([i for i in range(1, len(population)+1)])
    probabilities_2_be_selected = [i / d for i in range(1, len(population) + 1)]
    results = random.choices(population, weights=probabilities_2_be_selected, k=selection)
    return population, probabilities_2_be_selected, results

#TODO create functions (a) crossover and (b) mutations based on probabilities, (c) function which creates evolution
# process of generationg population, selecting (how much?) elements, (d) transforming (what share?) some with crossover
# and mutation and continue till limit (what is the limit?)


shift = 10
hours = 6
length = 200
# my_arr = fill_shift(shift, hours)
# print(tabulate(my_arr))
# diff_arr = fitness(hours, my_arr)
# print(diff_arr)
c = generate_population(length, shift, hours)

print(fitness(hours, c[0][0]), ' ', fitness(hours, c[0][-1]))

print('\n')
for y in c[2]:
    print(fitness(hours, y), end=' ')

