from random import choice
from copy import deepcopy

from utils import load_data_from_file, load_solution_from_file, plot_solutions, pprint


def local_solve(data_filename, solution_filename=None, plot_result=True):
    print('Local research solving...')
    print('Loading data from file...')
    camera_configurations, works_of_art = load_data_from_file(data_filename)
    max_movements = 500

    print('Generating_first_solution...')
    reference_solution = (
        load_solution_from_file(solution_filename, camera_configurations)
        if solution_filename
        else generate_simple_solution(camera_configurations, works_of_art)
    )
    current_cost = objective_function(reference_solution)

    print('Starting local research...')
    i = 0
    while i <= max_movements:
        new_solution = choose_next_solution(
            deepcopy(reference_solution),
            camera_configurations,
            works_of_art
        )
        reference_solution = choose_best_solution(
            deepcopy(reference_solution),
            deepcopy(new_solution)
        )

        new_cost = objective_function(reference_solution)
        if new_cost < current_cost:
            print('New cost: {}'.format(new_cost))
            current_cost = new_cost
            i = 0
        else:
            i += 1

    if plot_result:
        print('Total cost found: {}'.format(objective_function(reference_solution)))
        print('Plotting results...')
        plot_solutions(works_of_art, reference_solution)
        pprint(reference_solution, camera_configurations)

    return reference_solution


def objective_function(cameras):
    return sum(price for _, price, _, _ in cameras)


def generate_simple_solution(camera_configurations, works_of_art):
    return [min(camera_configurations, key=lambda x: x[0]) + (x, y) for x, y in works_of_art]


def choose_best_solution(solution_1, solution_2):
    return (
        solution_1
        if objective_function(solution_1) <= objective_function(solution_2)
        else solution_2
    )


def choose_next_solution(solution, camera_configurations, works_of_art):
    height = max(works_of_art, key=lambda x: x[0])[0]
    width = max(works_of_art, key=lambda x: x[1])[1]
    possible_positions = list(zip(range(height + 1), range(width + 1)))

    new_camera = choice(camera_configurations) + choice(possible_positions)
    new_radius, new_price, new_x, new_y = new_camera
    new_covered_works = get_covered_works([new_camera], works_of_art)

    concurrent_cameras = [
        (radius, price, x, y)
        for radius, price, x, y in solution
        if (x - new_x) ** 2 + (y - new_y) ** 2 <= (new_radius + radius) ** 2
    ]

    impacted_works = get_covered_works(concurrent_cameras, works_of_art)

    solution.append((new_radius, new_price, new_x, new_y))

    while new_covered_works != impacted_works:
        new_covered_works.update(get_covered_works(concurrent_cameras.pop(), works_of_art))

    for camera in concurrent_cameras:
        solution.remove(camera)

    return solution


def get_covered_works(cameras, works_of_art):
    covered_works = set()
    if isinstance(cameras, tuple):
        cameras = [cameras]
    for radius, _, camera_x, camera_y in cameras:
        covered_works.update(
            (x, y)
            for x in range(camera_x - radius, camera_x + radius + 1)
            for y in range(camera_y - radius, camera_y + radius + 1)
            if (
                (x, y) in works_of_art and
                (camera_x - x) ** 2 + (camera_y - y) ** 2 <= radius ** 2
            )
        )
    return covered_works
