"""
Author: Thibaut Seys
Last modified: 07/02/2018

This files implement the cli for our problem.

Usages:
    museum_solver.py <data_filename> linear
    museum_solver.py <data_filename> local [solution_filename]

Arguments:
    data_filename: [Mandatory] filename of the data file
    solver_type: [Mandatory] 'linear' or 'local'
    solution_filename: [Optional] filename of the solution file to explore with local research
"""
from sys import argv

from linear_museum_solver import linear_solve
from local_museum_solver import local_solve


if __name__ == '__main__':
    data_filename = argv[1]
    solver_type = argv[2]
    try:
        solution_filename = argv[3]
    except IndexError:
        solution_filename = None

    if solver_type == 'linear':
        linear_solve(data_filename)
    elif solver_type == 'local':
        local_solve(data_filename, solution_filename)
    else:
        print('Wrong input ({}) : \'linear\' or \'local\' expected.'.format(solver_type))
