import math
import random


def distance(point_1=(0, 0), point_2=(0, 0)) -> float:
    """
    Function to calculate the distance between two points
    :param point_1: tuple containing the x and y coordinates of the first point
    :param point_2: tuple containing the x and y coordinates of the second point
    :return: distance between the two points
    """
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def random_velocity(speed=100) -> [float, float]:
    """
    Function to generate a random velocity vector
    :param speed: speed of the object
    :return: velocity vector as a list
    """
    dir_x = random.uniform(-100, 100)
    dir_y = random.uniform(-100, 100)
    mag = math.sqrt(dir_x**2 + dir_y**2)

    if mag != 0:
        dir_x /= mag
        dir_y /= mag

    velocity_x = dir_x * speed
    velocity_y = dir_y * speed
    return [velocity_x, velocity_y]


def compute_velocity(speed, source_x, source_y, target_x, target_y) -> [float, float]:
    """
    Function to compute the velocity vector of an object
    :param speed: speed of the object
    :param source_x: x coordinate of the source object
    :param source_y: y coordinate of the source object
    :param target_x: x coordinate of the target object
    :param target_y: y coordinate of the target object
    :return: velocity vector as a list
    """
    dir_x = target_x - source_x
    dir_y = target_y - source_y
    mag = math.sqrt(dir_x**2 + dir_y**2)

    if mag != 0:
        dir_x /= mag
        dir_y /= mag

    velocity_x = dir_x * speed
    velocity_y = dir_y * speed
    return [velocity_x, velocity_y]
