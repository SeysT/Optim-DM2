import matplotlib.pyplot as plt


def load_data_from_file(data_filename):
    with open(data_filename, 'r') as data_file:
        data = data_file.read().strip().split('\n')

    camera_radius = [int(elt) for elt in data[0].split(',')]
    camera_prices = [int(elt) for elt in data[1].split(',')]

    cameras = list(zip(camera_radius, camera_prices))

    works_of_art = [
        (int(coordinates.split(',')[0]), int(coordinates.split(',')[1]))
        for coordinates in data[2:]
    ]

    return cameras, works_of_art


def plot_solutions(works_of_art, cameras):
    x_works, y_works = zip(*works_of_art)

    plt.title('Solution')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.plot([], [], 'ro', label='works')
    plt.plot([], [], 'bo', label='cameras')

    for radius, _, x, y in cameras:
        plt.gcf().gca().add_artist(
            plt.Circle((x, y), radius, edgecolor='b')
        )

    plt.plot(x_works, y_works, 'ro', markersize=1)

    plt.legend()
    plt.show()


def pprint(cameras, camera_configurations):
    for radius, price, x, y in cameras:
        print('{},{},{}'.format(camera_configurations.index((radius, price)) + 1, x, y))
