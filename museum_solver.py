from sys import argv

from linear_museum_solver import linear_solve
from local_museum_solver import local_solve


if __name__ == '__main__':
    solver_type = argv[2]
    data_filename = argv[1]

    if solver_type == 'linear':
        linear_solve(data_filename)
    elif solver_type == 'local':
        local_solve(data_filename)
    else:
        print('Wrong input ({}) : \'linear\' or \'local\' expected.'.format(solver_type))
