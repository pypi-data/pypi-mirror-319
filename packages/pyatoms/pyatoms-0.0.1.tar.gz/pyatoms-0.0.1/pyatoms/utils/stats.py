import matplotlib as mpl
import numpy as np

mpl.use('Agg')
from matplotlib import pyplot as plt
from prettytable import PrettyTable


def plot_distributions(arrays, names):
    if len(arrays) != len(names):
        raise ValueError("The number of arrays and names must be equal")

    fig, axs = plt.subplots(len(arrays), 1, figsize=(10, 5 * len(arrays)))

    for i, (array, name) in enumerate(zip(arrays, names)):
        axs[i].hist(array, bins=10, alpha=0.7, label=name)
        axs[i].legend(loc='upper right')
        
        stats_table = compute_statistics(array)
        table_text = axs[i].table(cellText=[[cell] for cell in stats_table.split('\n')],
                                  colWidths=[1.0],
                                  cellLoc='center',
                                  loc='right',
                                  bbox=[1.1, 0, 0.5, 1])
        table_text.auto_set_font_size(False)
        table_text.set_fontsize(8)
        
    plt.tight_layout()
    fig.savefig('./result.png')


def adjusted_r2(ndarray_1, ndarray_2, num_observation, num_independent_variable):
    return 1-(num_observation-1)/(num_observation-num_independent_variable-1)*(1-r2(ndarray_1, ndarray_2))


def r2(ndarray_1, ndarray_2):
    return 1-np.sum(np.square(ndarray_1-ndarray_2))/np.sum(np.square(ndarray_1-np.mean(ndarray_1)))


def rmse(ndarray_1, ndarray_2):
    return np.sqrt(np.mean(np.square(ndarray_1-ndarray_2)))


def mse(ndarray_1, ndarray_2):
    return np.mean(np.square(ndarray_1-ndarray_2))


def mae(ndarray_1, ndarray_2):
    return np.mean(np.abs(ndarray_1-ndarray_2))


def compute_statistics(data):
    """By ChatGPT-4"""
    if not isinstance(data, np.ndarray):
        raise ValueError("Input should be a numpy ndarray")

    mean_value = np.mean(data)
    median_value = np.median(data)
    variance_value = np.var(data)
    std_dev_value = np.std(data)
    min_value = np.min(data)
    max_value = np.max(data)
    quartiles_value = np.percentile(data, [25, 50, 75])
    sum_value = np.sum(data)

    table = PrettyTable()
    
    table.field_names = ["Statistic", "Value"]
    
    table.add_row(["Mean", f"{mean_value:.4E}"])
    table.add_row(["Median", f"{median_value:.4E}"])
    table.add_row(["Variance", f"{variance_value:.4E}"])
    table.add_row(["Standard Deviation", f"{std_dev_value:.4E}"])
    table.add_row(["Min", f"{min_value:.4E}"])
    table.add_row(["Max", f"{max_value:.4E}"])
    table.add_row(["Quartile 25%", f"{quartiles_value[0]:.4E}"])
    table.add_row(["Quartile 50%", f"{quartiles_value[1]:.4E}"])
    table.add_row(["Quartile 75%", f"{quartiles_value[2]:.4E}"])
    table.add_row(["Sum", f"{sum_value:.4E}"])
    
    return str(table)
