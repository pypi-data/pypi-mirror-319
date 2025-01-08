import numpy as np


def group_by_tol(array, tol=1E-05, key=None):
    if key == None:
        key = lambda a: a
    
    array = sorted(array, key=key)
    
    group = [[]]
    
    first_num = key(array[0])
    current_group = group[0]
    
    for i in array:
        current_num = key(i)
        
        if (current_num - first_num) < tol:
            current_group.append(i)
        else:
            group.append([])
            current_group = group[-1]
            current_group.append(i)
            first_num = key(i)
    
    return group


def is_integer(num, tol=1E-08):
    num = float(num)
    
    return abs(num - round(num)) < tol


def calc_parallelogram_area_defined_by_two_vector(vector_1, vector_2):
    return np.linalg.norm(np.cross(vector_1, vector_2))


def calc_angle_between_two_vector(vector_1, vector_2, fmt='rad'):
    radian = np.arccos(np.dot(vector_1, vector_2)/(np.linalg.norm(vector_1)*np.linalg.norm(vector_2)))
    
    if fmt == 'deg':
        return np.rad2deg(radian)
    elif fmt == 'rad':
        return radian
    else:
        raise ValueError(
            "calc_angle_between_two_vector: fmt is neither 'deg' nor 'rad'. fmt: %s" % (fmt)
        )
