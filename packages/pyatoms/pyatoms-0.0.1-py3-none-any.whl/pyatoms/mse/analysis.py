import itertools
import math
import os
import warnings
from copy import deepcopy
from os.path import join

import matplotlib as mpl
import numpy as np
import statsmodels.api as sm
from pymatgen.core.composition import Composition

mpl.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

from pyatoms.mse.composition import (get_composition_dict,
                                     get_composition_latex_str)
from pyatoms.utils.file import rm_fr_atomic
from pyatoms.utils.mathlib import calc_parallelogram_area_defined_by_two_vector
from pyatoms.utils.plot import get_proper_limit


class BandPlotter:
    def __init__(self):
        self.data_up = None
        self.data_dw = None
        self.data_x_range = None
        self.vbm = None
        self.cbm = None
        self.label = None
    
    def read_data_from_reformatted_band_dat(self, path_dir):
        listdir = os.listdir(path_dir)
        
        if ('REFORMATTED_BAND_UP.dat' in listdir) and ('REFORMATTED_BAND_DW.dat' in listdir):
            data_up = np.loadtxt(join(path_dir, 'REFORMATTED_BAND_UP.dat'))
            data_dw = np.loadtxt(join(path_dir, 'REFORMATTED_BAND_DW.dat'))
        elif 'REFORMATTED_BAND.dat' in listdir:
            data_up = np.loadtxt(join(path_dir, 'REFORMATTED_BAND.dat'))
            data_dw = np.loadtxt(join(path_dir, 'REFORMATTED_BAND.dat'))
        else:
            raise Exception(
                'materials_science_utils.BandPlotter.read_data_from_reformatted_band_dat: missing necessary files (REFORMATTED_BAND)!'
            )
        
        self.data_up = []
        for i in range(data_up.shape[1]-1):
            self.data_up.append([data_up[:, 0], data_up[:, i+1]])
        
        self.data_dw = []
        for i in range(data_dw.shape[1]-1):
            self.data_dw.append([data_dw[:, 0], data_dw[:, i+1]])
    
    def process_data(self):
        self.data_x_range = []
        xmin = []
        for i in self.data_up:
            xmin.append(min(i[0]))
        for i in self.data_dw:
            xmin.append(min(i[0]))
        xmax = []
        for i in self.data_up:
            xmax.append(max(i[0]))
        for i in self.data_dw:
            xmax.append(max(i[0]))
        self.data_x_range = [min(xmin), max(xmax)]
        
        self.vbm = []
        self.cbm = []
        vbm = []
        cbm = []
        for i in self.data_up:
            zipped = zip(*i)
            for j in zipped:
                if j[1] > 0:
                    vbm.append(j)
                if j[1] < 0:
                    cbm.append(j)
        for i in self.data_dw:
            zipped = zip(*i)
            for j in zipped:
                if j[1] > 0:
                    vbm.append(j)
                if j[1] < 0:
                    cbm.append(j)
        vbm = sorted(vbm, key=lambda a: a[1])
        cbm = sorted(cbm, key=lambda a: a[1])
        cbm.reverse()
        for i in vbm:
            if np.isclose(i[1], vbm[0][1]):
                self.vbm.append(i)
        for i in cbm:
            if np.isclose(i[1], cbm[0][1]):
                self.cbm.append(i)
    
    def read_label_from_klabels(self, path_dir):
        with open(join(path_dir, 'KLABELS')) as f:
            content = f.readlines()
        
        self.label = [[i.strip().split()[0], float(i.strip().split()[1])] for i in content[1:-3]]
        
        mapping_from_txt_to_latex = {
            'Gamma': r'\Gamma', 
            'DELTA': r'\Delta', 
        }
        
        for i in self.label:
            for j in mapping_from_txt_to_latex.keys():
                if j in i[0]:
                    i[0] = '%s%s%s' % (i[0].split(sep=j)[0], mapping_from_txt_to_latex[j], i[0].split(sep=j)[1])
        
        self.label = sorted(self.label, key=lambda a: a[1])
    
    def plot(self, path_saving, title=None, spin=True, ylim=(-2.50, 2.50), rotate_xtick=False, vbm_cbm=False):
        self.process_data()
        
        # ----------
        
        fig_size = (10, 10/8*6)
        
        colour_up = 'red'
        colour_dw = 'orange'
        
        linestyle_up = '-'
        linestyle_dw = '--'
        
        linewidth_up = 2
        linewidth_dw = 2
        
        title_fontsize = 40
        title_padding = 20
        
        label_fontsize = 40
        x_label_padding = 5
        y_label_padding = 5
        
        tick_fontsize = 28.8
        tick_padding = 10
        tick_width = 2
        
        spine_width = 2
        
        grid_width = 2
        
        vbm_cbm_size = 150
        
        # ----------
        
        # font setting
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['mathtext.fontset'] = 'cm'

        # initializing
        fig, ax = plt.subplots(figsize=fig_size, constrained_layout=True)
        
        # plotting
        for i in self.data_up:
            ax.plot(i[0], i[1], color=colour_up, linestyle=linestyle_up, linewidth=linewidth_up)
        
        if spin:
            for i in self.data_dw:
                ax.plot(i[0], i[1], color=colour_dw, linestyle=linestyle_dw, linewidth=linewidth_dw)
        
        ax.plot(self.data_x_range, [0, 0], color='black', linestyle='--', linewidth=grid_width)
        
        for i in self.label[1:-1]:
            if '|' in i[0]:
                ax.plot([i[1], i[1]], ylim, color='white', linestyle='-', linewidth=max(linewidth_up, linewidth_dw)+2, zorder=10000)
                ax.plot([i[1], i[1]], ylim, color='black', linestyle='--', linewidth=grid_width, zorder=10001)
            else:
                ax.plot([i[1], i[1]], ylim, color='black', linestyle='--', linewidth=grid_width)
        
        if vbm_cbm:
            for i in self.cbm:
                ax.scatter(i[0], i[1], s=vbm_cbm_size, color='black', marker='o', zorder=10002)
            for i in self.vbm:
                ax.scatter(i[0], i[1], s=vbm_cbm_size, color='black', marker='o', zorder=10002)
        
        # formatting
        if title != None:
            ax.set_title(title, fontsize=title_fontsize, pad=title_padding, fontweight='bold')
        
        ax.set_xlabel(r'Wave Vector', fontsize=label_fontsize, labelpad=x_label_padding, fontweight='bold')
        ax.set_ylabel(r'E - E$\mathbf{_{fermi}}$ (eV)', fontsize=label_fontsize, labelpad=y_label_padding, fontweight='bold')

        ax.set_xlim(self.data_x_range[0], self.data_x_range[1])
        ax.set_ylim(ylim[0], ylim[1])
        
        xtick_label = [i[0] for i in self.label]
        xtick = [i[1] for i in self.label]
        xtick_label = [r'$\mathrm{%s}$' % i for i in xtick_label]
        ax.set_xticks(xtick)
        if rotate_xtick:
            ax.set_xticklabels(xtick_label, rotation=90)
        else:
            ax.set_xticklabels(xtick_label)
        
        ax.tick_params(labelsize=tick_fontsize, pad=tick_padding, width=tick_width)
        ax.tick_params(bottom=True, top=False, left=True, right=False)
        
        ax.spines['top'].set_linewidth(spine_width)
        ax.spines['bottom'].set_linewidth(spine_width)
        ax.spines['left'].set_linewidth(spine_width)
        ax.spines['right'].set_linewidth(spine_width)
        
        fig.savefig(path_saving, dpi=300)


def read_eladat(path_eladat):
    with open(path_eladat) as f:
        content = [i.strip() for i in f.readlines()]
        
    data = {}
    
    data['Elastic tensor'] = [[float(j) for j in i.split()] for i in content[2:2+6]]
    data['Compliance tensor'] = [[float(j) for j in i.split()] for i in content[11:11+6]]
    data["Young's modulus"] = {
        'Voigt approximate': float(content[20].split()[2]), 
        'Reuss approximate': float(content[21].split()[2]), 
        'Hill approximate': float(content[22].split()[3]), 
    }
    data['Shear modulus'] = {
        'Voigt approximate': float(content[20].split()[3]), 
        'Reuss approximate': float(content[21].split()[3]), 
        'Hill approximate': float(content[22].split()[4]), 
    }
    data['Bulk modulus'] = {
        'Voigt approximate': float(content[20].split()[4]), 
        'Reuss approximate': float(content[21].split()[4]), 
        'Hill approximate': float(content[22].split()[5]), 
    }
    data['Poisson ratio'] = {
        'Voigt approximate': float(content[20].split()[5]), 
        'Reuss approximate': float(content[21].split()[5]), 
        'Hill approximate': float(content[22].split()[6]), 
    }
    data['Pugh ratio'] = float(content[24].split()[3])
    data['Cauchy pressure'] = float(content[25].split()[3])
    data['Chung-Buessem Anisotropy Index'] = float(content[29].split()[4])
    data['Universal Elastic Anisotropy Index'] = float(content[30].split()[5])
    data['Elastic Stability Conditions'] = content[32].split()[3]
    
    return data


class BinaryPhaseDiagramAnalysis:
    def __init__(self, phase_diagram, order):
        self.phase_diagram = None
        self.order = None
        self.line_coord = None
        self.stable_composition_and_coord = None
        self.fig = None
        self.ax = None
        
        self.phase_diagram = deepcopy(phase_diagram)
        self.order = order
    
    def get_line(self):
        qhull_entry = self.phase_diagram.qhull_entries
        qhull_data = np.array(self.phase_diagram.qhull_data)
        line = self.uniquelines(self.phase_diagram.facets)
        
        self.line_coord = []
        for i in line:
            coord = np.array(
                [
                [qhull_data[i[0], 0], self.phase_diagram.get_form_energy_per_atom(qhull_entry[i[0]])], 
                [qhull_data[i[1], 0], self.phase_diagram.get_form_energy_per_atom(qhull_entry[i[1]])]
                ]
            )
            self.line_coord.append(coord)
    
    def get_stable_composition_and_coord(self):
        qhull_entry = self.phase_diagram.qhull_entries
        qhull_data = np.array(self.phase_diagram.qhull_data)
        line = self.uniquelines(self.phase_diagram.facets)
        
        stable_idx = set()
        for i in line:
            stable_idx.update(i)
        
        self.stable_composition_and_coord = []
        for i in stable_idx:
            composition = qhull_entry[i].composition
            coord = np.array([qhull_data[i, 0], self.phase_diagram.get_form_energy_per_atom(qhull_entry[i])])
            
            self.stable_composition_and_coord.append([composition, coord])
    
    # TODO: This method is not correct!
    def get_coord(self, composition):
        entry = [i for i in self.phase_diagram.all_entries if (i.composition.reduced_composition==Composition(composition).reduced_composition)]
        coord = [[composition.get_atomic_fraction(self.order[0]), self.phase_diagram.get_form_energy_per_atom(i)] for i in entry]
        return coord
    
    def get_energy_above_hull(self, composition):
        entry = [i for i in self.phase_diagram.all_entries if (i.composition.reduced_composition==Composition(composition).reduced_composition)]
        e_hull = [self.phase_diagram.get_decomp_and_e_above_hull(i)[1] for i in entry]
        return e_hull
    
    def plot(self):
        # ----------
        
        fig_size = (10, 10)
        
        line_color = 'black'
        line_width = 4
        
        scatter_size = 200
        scatter_color = 'black'
        scatter_marker = 'o'
        scatter_edge_color = 'black'
        scatter_line_width = 0.1
        
        spine_width = 3

        title_fontsize = 48
        title_padding = 20

        label_fontsize = 48
        label_padding = 5

        tick_fontsize = 44
        tick_padding = 10
        tick_width = 3
        
        # ----------
        
        # font setting
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['mathtext.fontset'] = 'cm'
        
        self.fig, self.ax = plt.subplots(figsize=fig_size, constrained_layout=True)
        fig = self.fig
        ax = self.ax
        
        for i in self.line_coord:
            ax.plot(
                [i[0][0], i[1][0]], 
                [i[0][1], i[1][1]], 
                c=line_color, 
                lw=line_width, 
            )
        
        print('stable_composition:')
        for i in self.stable_composition_and_coord:
            print(i[0])
            ax.scatter(
                [i[1][0]], 
                [i[1][1]], 
                s=scatter_size, 
                c=scatter_color, 
                marker=scatter_marker, 
                edgecolors=scatter_edge_color, 
                linewidths=scatter_line_width, 
                zorder=1E08, 
            )
        
        ax.set_title('%s-%s System' % (self.order[0], self.order[1]), fontsize=title_fontsize, pad=title_padding, fontweight='bold')

        ax.set_xlabel('%s %%at' % (self.order[0]), fontsize=label_fontsize, labelpad=label_padding, fontweight='bold')
        ax.set_ylabel(r'E$\mathbf{_{f}}$ per Atom (eV)', fontsize=label_fontsize, labelpad=label_padding, fontweight='bold')
        
        ax.spines['top'].set_linewidth(spine_width)
        ax.spines['bottom'].set_linewidth(spine_width)
        ax.spines['left'].set_linewidth(spine_width)
        ax.spines['right'].set_linewidth(spine_width)
        
        ax.tick_params(labelsize=tick_fontsize, pad=tick_padding, width=tick_width)
        ax.tick_params(bottom=True, top=False, left=True, right=False)
    
    def add_text(self, composition, shift, e_hull=False):
        # ----------
        
        font_size = 44
        font_color = 'black'
        
        # ----------
        
        fig = self.fig
        ax = self.ax
        
        if type(composition) == type([]):
            composition = composition[0]
            idx = composition[1]
        else:
            idx = 0
        
        composition_dict = get_composition_dict(composition)
        latex_string = get_composition_latex_str(composition_dict)
        
        if e_hull:
            value_e_hull = self.get_energy_above_hull(composition)
            if len(value_e_hull) > 1:
                warnings.warn(
                    'materials_science_utils.PhaseDiagramAnalyser.add_meta_stable: len(value_e_hull) > 1, value_e_hull: %s, composition: %s' % (value_e_hull, composition), 
                    UserWarning, 
                )
            value_e_hull = value_e_hull[idx]
            
            latex_string += '\n'
            latex_string += '%.3f' % (value_e_hull)
            latex_string += 'eV'
        
        coord = np.array(self.get_coord(Composition(composition))[idx])
        coord += np.array(shift)
        
        ax.text(
            coord[0], 
            coord[1], 
            latex_string, 
            fontsize=font_size, 
            color=font_color, 
            ha='center', 
            va='top', 
        )
    
    def save(self, path_saving, dpi=300):
        self.fig.savefig(path_saving, dpi=dpi)
    
    @staticmethod
    def uniquelines(q):
        setoflines = set()
        for facets in q:
            for line in itertools.combinations(facets, 2):
                setoflines.add(tuple(sorted(line)))
        return setoflines


class TernaryPhaseDiagramAnalysis:
    # The order should be determined according to pd.qhull_data and pd.qhull_entries! Very bad!
    # TODO: We should simplified this!
    def __init__(self, phase_diagram, order):
        self.phase_diagram = None
        self.order = None
        self.line_coord = None
        self.stable_composition_and_coord = None
        self.fig = None
        self.ax = None
        
        self.phase_diagram = deepcopy(phase_diagram)
        self.order = order
    
    def get_line(self):
        qhull_entry = self.phase_diagram.qhull_entries
        qhull_data = np.array(self.phase_diagram.qhull_data)
        line = self.uniquelines(self.phase_diagram.facets)
        
        self.line_coord = []
        for i in line:
            coord = self.triangular_coord(qhull_data[i, 0:2])
            self.line_coord.append(coord)
    
    def get_stable_composition_and_coord(self):
        qhull_entry = self.phase_diagram.qhull_entries
        qhull_data = np.array(self.phase_diagram.qhull_data)
        line = self.uniquelines(self.phase_diagram.facets)
        
        stable_idx = set()
        for i in line:
            stable_idx.update(i)
        
        self.stable_composition_and_coord = []
        for i in stable_idx:
            composition = qhull_entry[i].composition
            coord = self.triangular_coord(qhull_data[i, 0:2])
            
            coord_2 = self.get_triangular_coord(composition)
            assert abs(coord[0]-coord_2[0])<1E-05 and abs(coord[1]-coord_2[1])<1E-05, 'PhaseDiagramAnalyser: not(abs(coord[0]-coord_2[0])<1E-05 and abs(coord[1]-coord_2[1])<1E-05)'
            
            self.stable_composition_and_coord.append([composition, coord])
    
    def get_triangular_coord(self, composition):
        coord = [composition.get_atomic_fraction(self.order[0]), composition.get_atomic_fraction(self.order[1])]
        return self.triangular_coord(coord)
    
    def get_energy_above_hull(self, composition):
        entry = [i for i in self.phase_diagram.all_entries if (i.composition.reduced_composition==Composition(composition).reduced_composition)]
        e_hull = [self.phase_diagram.get_decomp_and_e_above_hull(i)[1] for i in entry]
        return e_hull
    
    def plot(self):
        # ----------
        
        fig_size = (10, 10)
        
        line_color = 'black'
        line_width = 4
        
        scatter_size = 200
        scatter_color = 'black'
        scatter_marker = 'o'
        scatter_edge_color = 'black'
        scatter_line_width = 0.1
        
        title_fontsize = 48
        title_padding = 20
        
        # ----------
        
        # font setting
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['mathtext.fontset'] = 'cm'
        
        self.fig, self.ax = plt.subplots(figsize=fig_size, constrained_layout=True)
        fig = self.fig
        ax = self.ax
        
        ax.set_axis_off()
        ax.set_aspect('equal')
        
        for i in self.line_coord:
            ax.plot(
                [i[0][0], i[1][0]], 
                [i[0][1], i[1][1]], 
                c=line_color, 
                lw=line_width, 
            )
        
        print('stable_composition:')
        for i in self.stable_composition_and_coord:
            print(i[0])
            ax.scatter(
                [i[1][0]], 
                [i[1][1]], 
                s=scatter_size, 
                c=scatter_color, 
                marker=scatter_marker, 
                edgecolors=scatter_edge_color, 
                linewidths=scatter_line_width, 
                zorder=1E08, 
            )
        
        ax.set_title('%s-%s-%s System' % (self.order[0], self.order[1], self.order[2]), fontsize=title_fontsize, pad=title_padding, fontweight='bold')
    
    def add_meta_stable(self, composition, idx, max_e_hull=0.05):
        # ----------
        
        min_e_hull = 0.00
        max_e_hull = max_e_hull
        
        min_color = 'yellow'
        max_color = 'red'
        
        scatter_size = 25
        scatter_marker = 'o'
        scatter_edge_color = 'black'
        scatter_line_width = 0.1
        
        # ----------
        
        fig = self.fig
        ax = self.ax
        
        color = [min_color, max_color]
        cmap = LinearSegmentedColormap.from_list("custom_cmap", color, N=256)
        norm = Normalize(vmin=min_e_hull, vmax=max_e_hull)
        
        coord = self.get_triangular_coord(composition)
        e_hull = self.get_energy_above_hull(composition)
        if len(e_hull) > 1:
            warnings.warn(
                'materials_science_utils.PhaseDiagramAnalyser.add_meta_stable: len(e_hull) > 1, e_hull: %s, composition: %s' % (e_hull, composition), 
                UserWarning, 
            )
        e_hull = e_hull[idx]
        
        if e_hull < max_e_hull:
            scatter = ax.scatter(
                [coord[0]], 
                [coord[1]], 
                s=scatter_size, 
                c=e_hull, 
                marker=scatter_marker, 
                edgecolors=scatter_edge_color, 
                linewidths=scatter_line_width, 
                zorder=1E08, 
                cmap=cmap, 
                norm=norm, 
            )
            # fig.colorbar(scatter)
    
    def add_text(self, composition, shift, e_hull=False):
        # ----------
        
        font_size = 8
        font_color = 'black'
        
        # ----------
        
        fig = self.fig
        ax = self.ax
        
        if type(composition) == type([]):
            composition = composition[0]
            idx = composition[1]
        else:
            idx = 0
        
        composition_dict = get_composition_dict(composition)
        latex_string = get_composition_latex_str(composition_dict)
        
        if e_hull:
            value_e_hull = self.get_energy_above_hull(composition)
            if len(value_e_hull) > 1:
                warnings.warn(
                    'materials_science_utils.PhaseDiagramAnalyser.add_meta_stable: len(value_e_hull) > 1, value_e_hull: %s, composition: %s' % (value_e_hull, composition), 
                    UserWarning, 
                )
            value_e_hull = value_e_hull[idx]
            
            latex_string += '\n'
            latex_string += '%.3f' % (value_e_hull)
            latex_string += 'eV'
        
        coord = np.array(self.get_triangular_coord(composition))
        coord += np.array(shift)
        
        ax.text(
            coord[0], 
            coord[1], 
            latex_string, 
            fontsize=font_size, 
            color=font_color, 
            ha='center', 
            va='top', 
        )
    
    def save(self, path_saving, dpi=300):
        self.fig.savefig(path_saving, dpi=dpi)
    
    @staticmethod
    def uniquelines(q):
        setoflines = set()
        for facets in q:
            for line in itertools.combinations(facets, 2):
                setoflines.add(tuple(sorted(line)))
        return setoflines

    @staticmethod
    def triangular_coord(coord):
        unit_vec = np.array([[1, 0], [0.5, math.sqrt(3) / 2]])
        result = np.dot(np.array(coord), unit_vec)
        return result


class SurfaceEnergyAnalysis:

    # Fiorentini, V., & Methfessel, M. (1996). 
    # Extracting convergent surface energies from slab calculations. 
    # Journal of Physics: Condensed Matter, 8(36), 6525.
    
    def __init__(self, num_layer, structure, energy, tol_area=1E-08, tol_comp=1E-08):
        # __init__
        self.num_layer = None
        self.structure = None
        self.energy = None
        self.surface_area = None
        self.mean_surface_area = None
        self.comp_dict_slope = None
        self.comp_dict_intercept = None
        
        # calc_surface_energy()
        self.fitted_energy_for_unit_formula = None
        self.fitted_intercept = None
        self.r_squared = None
        self.surface_energy = None
        
        # calc_final_surface_energy_from_last_n_layer()
        self.final_surface_energy_method = None
        self.final_surface_energy = None
        self.final_surface_energy_joule = None
        
        if len(num_layer) == len(structure) == len(energy):
            zipped = zip(num_layer, structure, energy)
            zipped = sorted(zipped, key=lambda a: a[0])
            self.num_layer, self.structure, self.energy = zip(*zipped)
        else:
            raise ValueError(
                'materials_science_utils.SurfaceEnergy.__init__: not (len(num_layer) == len(structure) == len(energy))'
            )
        
        surface_area = [calc_parallelogram_area_defined_by_two_vector(i.lattice.matrix[0], i.lattice.matrix[1]) for i in self.structure]
        if (max(surface_area) - min(surface_area)) > tol_area:
            raise ValueError(
                'materials_science_utils.SurfaceEnergy.__init__: (max(surface_area) - min(surface_area)) > tol_area'
            )
        else:
            self.surface_area = surface_area
            self.mean_surface_area = sum(surface_area) / len(surface_area)
        
        comp_dict = [get_composition_dict(i.composition) for i in self.structure]
        comp_dict_slope = {i: (comp_dict[1][i]-comp_dict[0][i])/(self.num_layer[1]-self.num_layer[0]) for i in comp_dict[0].keys()}
        for i in range(2, len(self.num_layer)):
            slope = {j: (comp_dict[i][j]-comp_dict[i-1][j])/(self.num_layer[i]-self.num_layer[i-1]) for j in comp_dict[i-1].keys()}
            for j in slope.keys():
                if abs(slope[j] - comp_dict_slope[j]) > tol_comp:
                    raise ValueError(
                        'materials_science_utils.SurfaceEnergy.__init__: abs(slope[j] - comp_dict_slope[j]) > tol_comp'
                    )
        self.comp_dict_slope = comp_dict_slope
        self.comp_dict_intercept = {i: comp_dict[0][i] - self.comp_dict_slope[i]*self.num_layer[0] for i in comp_dict[0].keys()}
    
    def calc_surface_energy(self, chemical_potential=None, shift=0, r_squared_warning_threshold=0.99):
        y = np.array(deepcopy(self.energy))
        X = np.array(deepcopy(self.num_layer))
        X = sm.add_constant(X)
        
        model = sm.OLS(y, X)
        result = model.fit()
        
        self.fitted_energy_for_unit_formula = result.params[1]
        self.fitted_intercept = result.params[0]
        self.r_squared = result.rsquared
        
        if self.r_squared < r_squared_warning_threshold:
            warnings.warn(
                'materials_science_utils.SurfaceEnergyAnalysis.calc_surface_energy: self.r_squared < %.4f' % (r_squared_warning_threshold), 
                UserWarning, 
            )
        
        # calc surface energy
        surface_energy = []
        
        if chemical_potential == None:
            chemical_potential = {i: 0.00 for i in self.comp_dict_slope.keys()}
        
        comp_dict_using_chemical_potential = {i: self.comp_dict_intercept[i]-shift*self.comp_dict_slope[i] for i in self.comp_dict_slope.keys()}
        for idx, i in enumerate(self.num_layer):
            _surface_energy = self.energy[idx]
            _surface_energy -= ((i + shift) * self.fitted_energy_for_unit_formula)
            for j in comp_dict_using_chemical_potential.keys():
                _surface_energy -= comp_dict_using_chemical_potential[j] * chemical_potential[j]
            _surface_energy = _surface_energy / self.mean_surface_area / 2
            
            surface_energy.append(_surface_energy)
        
        self.surface_energy = surface_energy
    
    def calc_final_surface_energy_from_last_n_layer(self, n):
        if self.surface_energy == None:
            warnings.warn(
                'materials_science_utils.SurfaceEnergyAnalysis.calc_final_surface_energy_from_last_n_layer: Please execute method calc_surface_energy() first!', 
                UserWarning, 
            )
        else:
            if n > len(self.num_layer):
                raise ValueError(
                    'materials_science_utils.SurfaceEnergyAnalysis.calc_final_surface_energy_from_last_n_layer: n > len(self.num_layer), n: %s, len(self.num_layer): %s' % (n, len(self.num_layer))
                )
            
            self.final_surface_energy_method = {
                'method': 'calc_final_surface_energy_from_last_n_layer', 
                'n': n, 
            }
            
            self.final_surface_energy = sum(self.surface_energy[-n:]) / n
            self.final_surface_energy_joule = self.final_surface_energy * 16.0217662
    
    def plot_total_energy_vs_num_layer(self):
        if self.surface_energy == None:
            warnings.warn(
                'materials_science_utils.SurfaceEnergyAnalysis.plot_total_energy_vs_num_layer: Please execute method calc_surface_energy()', 
                UserWarning, 
            )
        else:
            # setting
            figsize = (10, 10)
            
            scatter_size = 60
            scatter_color = 'k'
            scatter_marker = 'o'
            
            extra_x = 0.20
            extra_y = 0.20
            
            percentage_x = True
            percentage_y = True
            
            line_color = 'k'
            line_width = 2
            line_style = '--'
            
            text_fontsize = 30
            shift_r_squared = [0.025, 0.025]
            shift_equation = [0.025, 0.100]
            
            with_title = False
            title = 'Total Energy Changes with the Number of Surface Layers'
            title_fontsize = 30
            title_padding = 10
            
            tick_fontsize = 25
            tick_padding = 10
            
            x_label = 'Layer Number'
            y_label = 'Total Energy (eV)'
            label_fontsize = 30
            label_padding = 10
            
            # font setting
            plt.rcParams['font.family'] = 'Times New Roman'
            plt.rcParams['mathtext.fontset'] = 'cm'

            # initializing
            fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
            
            # plotting
            ax.scatter([self.num_layer], [self.energy], s=scatter_size, c=scatter_color, marker=scatter_marker)
            
            pred_y = [self.fitted_intercept+self.fitted_energy_for_unit_formula*min(self.num_layer), self.fitted_intercept+self.fitted_energy_for_unit_formula*max(self.num_layer)]
            xlim, ylim = get_proper_limit(self.num_layer, pred_y, extra_x=extra_x, extra_y=extra_y, percentage_x=percentage_x, percentage_y=percentage_y)
            ax.plot(
                [xlim[0], xlim[1]], 
                [self.fitted_intercept+self.fitted_energy_for_unit_formula*xlim[0], self.fitted_intercept+self.fitted_energy_for_unit_formula*xlim[1]], 
                c=line_color, 
                lw=line_width, 
                ls=line_style, 
            )
            
            # texting
            ax.text(
                1-shift_r_squared[0], 
                1-shift_r_squared[1], 
                r'R$^2$ = %.4f' % (self.r_squared), 
                ha='right', 
                va='top', 
                fontsize=text_fontsize, 
                transform=ax.transAxes, 
            )
            ax.text(
                1-shift_equation[0], 
                1-shift_equation[1], 
                r'y = %.4f x + %.4f' % (self.fitted_energy_for_unit_formula, self.fitted_intercept), 
                ha='right', 
                va='top', 
                fontsize=text_fontsize, 
                transform=ax.transAxes, 
            )
            
            # formatting
            if with_title:
                ax.set_title(title, fontsize=title_fontsize, pad=title_padding)

            ax.set_xlabel(x_label, fontsize=label_fontsize, labelpad=label_padding)
            ax.set_ylabel(y_label, fontsize=label_fontsize, labelpad=label_padding)

            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)

            ax.tick_params(labelsize=tick_fontsize, pad=tick_padding)
            ax.tick_params(bottom=True, top=False, left=True, right=False)
            
            return fig, ax
    
    def plot_surface_energy_vs_num_layer(self, extra_y):
        if self.final_surface_energy == None:
            warnings.warn(
                'materials_science_utils.SurfaceEnergyAnalysis.plot_surface_energy_vs_num_layer: Please execute method calc_final_surface_energy_from_last_n_layer()', 
                UserWarning, 
            )
        else:
            # setting
            figsize = (10, 10)
            
            extra_x = 0.10
            
            percentage_x = True
            percentage_y = False
            
            line_color = 'k'
            line_width = 2
            line_style = '-'
            scatter_size = 8
            scatter_marker = 'o'
            
            final_line_color = 'k'
            final_line_width = 2
            final_line_style = '--'
            extra_percentage_final_line = 0.10
            
            text_fontsize = 30
            shift_joule = [0.025, 0.025]
            shift_ev = [0.025, 0.100]
            
            with_title = False
            title = 'Surface Energy Changes with the Number of Surface Layers'
            title_fontsize = 30
            title_padding = 10
            
            tick_fontsize = 25
            tick_padding = 10
            
            x_label = 'Layer Number'
            y_label = r'Surface Energy (eV / Å$^2$)'
            label_fontsize = 30
            label_padding = 10
            
            # font setting
            plt.rcParams['font.family'] = 'Times New Roman'
            plt.rcParams['mathtext.fontset'] = 'cm'

            # initializing
            fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
            
            # plotting
            ax.plot(
                self.num_layer, 
                self.surface_energy, 
                c=line_color, 
                lw=line_width, 
                ls=line_style, 
                marker=scatter_marker, 
                markersize=scatter_size, 
            )
            
            if self.final_surface_energy_method['method'] == 'calc_final_surface_energy_from_last_n_layer':
                num_layer_used = self.num_layer[-self.final_surface_energy_method['n']:]
                final_line_length = max(num_layer_used) - min(num_layer_used)
                ax.plot(
                    [min(num_layer_used)-final_line_length*extra_percentage_final_line, max(num_layer_used)+final_line_length*extra_percentage_final_line], 
                    [self.final_surface_energy, self.final_surface_energy], 
                    c=final_line_color, 
                    lw=final_line_width, 
                    ls=final_line_style, 
                )
            
            # texting
            ax.text(
                0.6+shift_ev[0], 
                1-shift_ev[1], 
                r'%.4f eV / Å$^2$' % (self.final_surface_energy), 
                ha='left', 
                va='top', 
                fontsize=text_fontsize, 
                transform=ax.transAxes, 
            )
            ax.text(
                0.6+shift_joule[0], 
                1-shift_joule[1], 
                r'%.4f J / m$^2$' % (self.final_surface_energy_joule), 
                ha='left', 
                va='top', 
                fontsize=text_fontsize, 
                transform=ax.transAxes, 
            )
            
            # formatting
            if with_title:
                ax.set_title(title, fontsize=title_fontsize, pad=title_padding)

            ax.set_xlabel(x_label, fontsize=label_fontsize, labelpad=label_padding)
            ax.set_ylabel(y_label, fontsize=label_fontsize, labelpad=label_padding)
            
            xlim, ylim = get_proper_limit(self.num_layer, self.surface_energy, extra_x=extra_x, extra_y=extra_y, percentage_x=percentage_x, percentage_y=percentage_y)
            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)
            
            ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.4f'))
            ax.tick_params(labelsize=tick_fontsize, pad=tick_padding)
            ax.tick_params(bottom=True, top=False, left=True, right=False)
            
            return fig, ax


def sort_structure_according_to_energy(structure, energy, name=None, path_dir_saving=False, with_idx=True):
    if not ((len(structure)==len(energy)) if name==None else (len(structure)==len(energy)==len(name))):
        raise ValueError('sort_structure_according_to_energy: structure, energy, and name should have the same length')
    
    if name == None:
        name = [str(i) for i in range(len(structure))]
    structure_energy_name = list(zip(structure, energy, name))
    structure_energy_name.sort(key=lambda a: a[1])
    sorted_structure = [i for i, j, k in structure_energy_name]
    sorted_name = [k for i, j, k in structure_energy_name]
    
    if path_dir_saving != False:
        rm_fr_atomic(path_dir_saving)
        os.mkdir(path_dir_saving)
        for idx, i in enumerate(sorted_structure):
            final_name = '%d_%s' % (idx, sorted_name[idx]) if with_idx else sorted_name[idx]
            i.to(fmt='poscar', filename=join(path_dir_saving, final_name))
    
    return sorted_structure, sorted_name
