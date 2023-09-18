import math

def distance(point_1=(0, 0), point_2=(0, 0)):
    """
    Function to calculate the distance between two points
    :param point_1: tuple containing the x and y coordinates of the first point
    :param point_2: tuple containing the x and y coordinates of the second point
    :return: distance between the two points
    """
    return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)