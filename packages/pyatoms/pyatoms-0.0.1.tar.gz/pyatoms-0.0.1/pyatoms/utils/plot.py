import numpy as np
from scipy.interpolate import (Akima1DInterpolator, CubicSpline,
                               PchipInterpolator, interp1d)


def interpolate_curve(x, y, method='cubic', num_point_for_plotting=1000):
    """
    :param points: x, y
    :param method: 'linear', 'cubic', 'pchip', 'akima'
    :return: x_plot, y_plot
    """
    x = np.array(x)
    y = np.array(y)
    
    x_plot = np.linspace(x.min(), x.max(), num_point_for_plotting)

    if method == 'linear':
        interp_func = interp1d(x, y, kind='linear')
    elif method == 'cubic':
        interp_func = CubicSpline(x, y)
    elif method == 'pchip':
        interp_func = PchipInterpolator(x, y)
    elif method == 'akima':
        interp_func = Akima1DInterpolator(x, y)
    else:
        raise ValueError("utils.interpolate_curve: unsupported method, please choose one from 'linear', 'cubic', 'pchip', 'akima'.")

    y_plot = interp_func(x_plot)
    
    return x_plot, y_plot


def get_proper_limit(x, y, extra_x=0.20, extra_y=0.20, percentage_x=True, percentage_y=True):
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    
    x_length = x_max - x_min
    y_length = y_max - y_min
    
    if percentage_x:
        x_lower_limit = x_min - x_length * extra_x
        x_upper_limit = x_max + x_length * extra_x
    else:
        x_lower_limit = x_min - extra_x
        x_upper_limit = x_max + extra_x
    
    if percentage_y:
        y_lower_limit = y_min - y_length * extra_y
        y_upper_limit = y_max + y_length * extra_y
    else:
        y_lower_limit = y_min - extra_y
        y_upper_limit = y_max + extra_y
    
    return (x_lower_limit, x_upper_limit), (y_lower_limit, y_upper_limit)
