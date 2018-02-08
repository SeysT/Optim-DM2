"""
Author: Thibaut Seys
Last modified: 07/02/2018

This file use the linear programming to modelize and solve our museum problems.

Model:
    + variables:
        We have one boolean variable per camera's type per position on our grid. If it is True,
        then we place this type of camera at this position.
    + constraint:
        For each work of art, we look at variables in range of the camera's radius. At least one
        of them should be True (the sum should be greater or equal to 1).
    + objective function:
        We want to minimize the total price of our cameras. This corresponds to the sum of our
        variables times the price of the camera type.

"""
from pyscipopt import Model, quicksum

from utils import load_data_from_file, plot_solutions, pprint


def linear_solve(data_filename, plot_result=True):
    print('Linear programming solving...')
    model = Model('Museum expo')

    print('Loading data from file...')
    camera_configurations, works_of_art = load_data_from_file(data_filename)
    height = max(works_of_art, key=lambda x: x[0])[0]
    width = max(works_of_art, key=lambda x: x[1])[1]

    print('Creating cameras variables...')
    camera_vars = {
        (radius, price, x, y): model.addVar('camera_{}_{}_{}'.format(radius, x, y), vtype='B')
        for x in range(height + 1)
        for y in range(width + 1)
        for radius, price in camera_configurations
    }

    print('Adding constraints for each work of art...')
    for work_x, work_y in works_of_art:
        possible_cameras = [
            (radius, price, x, y)
            for radius, price in camera_configurations
            for x in range(max(0, work_x - radius), min(height, work_x + radius) + 1)
            for y in range(max(0, work_y - radius), min(width, work_y + radius) + 1)
            if (work_x - x) ** 2 + (work_y - y) ** 2 <= radius ** 2
        ]
        model.addCons(
            quicksum(camera_vars[key] for key in possible_cameras) >= 1,
            'work_{}_{}'.format(work_x, work_y)
        )

    print('Setting the objective function...')
    model.setObjective(quicksum(
        var * price for (_, price, _, _), var in camera_vars.items()
    ), 'minimize')

    print('Optimizing our model...')
    model.optimize()

    if model.getStatus() != 'optimal':
        print('LP is not feasible')

        return None
    else:
        solution = [key for key, var in camera_vars.items() if model.getVal(var)]
        if plot_result:
            print('Total cost found: {}'.format(model.getObjVal()))

            print('Plotting results...')
            plot_solutions(works_of_art, solution)

            print('Formatted results:')
            pprint(solution, camera_configurations)

        return solution
