from itertools import product

import numpy as np
from ase.calculators.emt import EMT
from ase.mep.neb import NEB, idpp_interpolate
from ase.optimize import MDMin
from pymatgen.core.periodic_table import Element
from pymatgen.core.structure import Structure
from pymatgen.io.ase import AseAtomsAdaptor

from pyatoms.utils.mathlib import group_by_tol


def get_nearest_site(structure, idx_atom_0, element=None, considered_image=((0, 0, 0), )):
    if element == None:
        element = set(structure.species)
    else:
        element = set([Element(i) for i in element])
    
    site = []
    distance = []
    for i in considered_image:
        for idx_j, j in enumerate(structure):
            if j.specie in element:
                site.append((idx_j, tuple(i)))
                distance.append(structure[idx_atom_0].distance(j, i))
    
    return group_by_tol(zip(site, distance), tol=0.01, key=lambda a: a[1])


def get_structure_with_interstitial(structure, mesh, tol, element, idx_atom_0):
    structure_copy = structure.copy(
        properties=structure.properties, 
        site_properties=structure.site_properties, 
    )
    
    generator = insert_atom(
        structure=structure_copy, 
        mesh=mesh, 
        tol=tol, 
        element=element, 
        method_site_selection='all', 
        method_distance_calculation='pymatgen', 
    )
    
    frac_coord = None
    idx = 0
    for i in generator:
        if idx == idx_atom_0:
            frac_coord = i
            break
        idx += 1
    
    if frac_coord == None:
        raise ValueError(
            'materials_science_utils.get_structure_with_interstitial: frac_coord == None, maybe idx_atom_0 is greater than len(generator)'
        )
    
    idx_to_insert = get_idx_to_insert(structure_copy, element)
    
    structure_copy.insert(
        idx=idx_to_insert,
        species=element,
        coords=frac_coord,
        coords_are_cartesian=False,
        validate_proximity=False,
        properties=None,
        label=None,
    )
    
    return structure_copy


def get_idx_to_insert(structure, element):
    idx_to_insert = None
    for idx, i in enumerate(structure):
        if i.specie == Element(element):
            idx_to_insert = idx
            break
    
    if idx_to_insert == None:
        idx_to_insert = 0
    
    return idx_to_insert


def insert_atom(structure, mesh, tol, element='Li', method_site_selection='all', method_distance_calculation='pymatgen'):
    factor_tol_to_sphere_r = 1.10
    sphere_r = tol * factor_tol_to_sphere_r
    
    if method_site_selection not in ['all', 'sphere']:
        raise ValueError(
            "materials_science_utils.insert_atom: method_site_selection should be either 'all' or 'sphere', method_site_selection: %s" % (method_site_selection)
        )
    if method_distance_calculation not in ['numpy', 'pymatgen']:
        raise ValueError(
            "materials_science_utils.insert_atom: method_distance_calculation should be either 'numpy' or 'pymatgen', method_distance_calculation: %s" % (method_distance_calculation)
        )
    
    for i, j, k in product(range(mesh[0]), range(mesh[1]), range(mesh[2])):
        frac_coord = [i/mesh[0], j/mesh[1], k/mesh[2]]
        cart_coord = structure.lattice.get_cartesian_coords(frac_coord)
        
        if method_distance_calculation == 'numpy':
            structure = normalize_coordinate_by_point(structure, np.array(frac_coord))
        else:
            if method_site_selection == 'sphere':
                structure = normalize_coordinate_by_point(structure, np.array(frac_coord))
        
        lattice_matrix = structure.lattice.matrix
        
        idx_selected_site = []
        if method_site_selection == 'all':
            idx_selected_site = list(range(len(structure)))
        else:
            for idx_l, l in enumerate(structure):
                flag = True
                for m in range(3):
                    if abs(l.coords[m]-cart_coord[m]) > sphere_r:
                        flag = False
                        break
                
                if flag:
                    idx_selected_site.append(idx_l)
        
        distance = None
        if idx_selected_site != []:
            if method_distance_calculation == 'numpy':
                frac_coord_selected_site = np.array([structure[l].frac_coords for l in idx_selected_site])
                dx_frac = frac_coord_selected_site - frac_coord
                dx_cart = (
                    lattice_matrix[0] * dx_frac[:, 0:0+1] + 
                    lattice_matrix[1] * dx_frac[:, 1:1+1] + 
                    lattice_matrix[2] * dx_frac[:, 2:2+1]
                )
                distance = np.linalg.norm(dx_cart, axis=1)
            else:
                if method_site_selection == 'all':
                    structure.append(element, frac_coord)
                    distance = structure.distance_matrix[-1, :-1]
                    structure.pop(-1)
                else:
                    structure_only_selected_site = Structure(
                        lattice=structure.lattice,
                        species=[structure[i].species for i in idx_selected_site],
                        coords=[structure[i].frac_coords for i in idx_selected_site],
                    )
                    structure_only_selected_site.append(element, frac_coord)
                    distance = structure_only_selected_site.distance_matrix[-1, :-1]
        
        if (type(distance) == type(None)) or (min(distance) > tol):
            yield frac_coord


def get_idpp_interpolation(
    structure_ini, 
    structure_fin, 
    num_image, 
    normalize_fin=True, 
    fmax=0.1, 
    optimizer=MDMin, 
    mic=True, 
    steps=1000, 
    path_idpp_output_traj=None, 
    path_idpp_output_log=None, 
    min_distance=0.75, 
):
    if normalize_fin:
        structure_fin = normalize_coordinate_by_structure(structure_fin, structure_ini)
    
    ase_atoms_adaptor = AseAtomsAdaptor()
    
    atoms_ini = ase_atoms_adaptor.get_atoms(structure_ini)
    atoms_fin = ase_atoms_adaptor.get_atoms(structure_fin)
    
    atoms_ini.calc = EMT()
    atoms_fin.calc = EMT()
    
    image = [atoms_ini.copy() for i in range(num_image+1)]
    image.append(atoms_fin.copy())
    
    neb = NEB(image)
    neb.interpolate()
    idpp_interpolate(
        neb, 
        traj=path_idpp_output_traj, 
        log=path_idpp_output_log, 
        fmax=fmax,
        optimizer=optimizer, 
        mic=mic, 
        steps=steps, 
    )
    # neb.interpolate('idpp')
    
    interpolation = [ase_atoms_adaptor.get_structure(i) for i in image[1:-1]]
    
    assert len(interpolation) == num_image, 'materials_science_utils.get_idpp_interpolation: not (len(interpolation) == num_image)'
    
    if min_distance != None:
        for i in interpolation:
            distance_matrix = i.distance_matrix.copy()
            
            bool_index = np.ones_like(distance_matrix, dtype=bool)
            np.fill_diagonal(bool_index, False)
            
            off_diagonal_element = distance_matrix[bool_index]
            
            if off_diagonal_element.min() < min_distance:
                raise Exception(
                    'materials_science_utils.get_idpp_interpolation: off_diagonal_element.min() < min_distance, off_diagonal_element.min(): %f, min_distance: %f' % (off_diagonal_element.min(), min_distance)
                )
    
    return interpolation


def normalize_coordinate_by_point(input_structure, target_point_frac_coord):
    input_frac_coord = input_structure.frac_coords.copy()
    
    for idx, i in enumerate(input_frac_coord):
        input_site = i
        target_site = np.array(target_point_frac_coord)

        for j in range(3):
            while abs(input_site[j]+1-target_site[j]) < abs(input_site[j]-target_site[j]):
                input_site[j] += 1
            while abs(input_site[j]-1-target_site[j]) < abs(input_site[j]-target_site[j]):
                input_site[j] -= 1
    
    return Structure(
        lattice=input_structure.lattice,
        species=input_structure.species,
        coords=input_frac_coord,
        charge=input_structure.charge,
        validate_proximity=False,
        to_unit_cell=False,
        coords_are_cartesian=False,
        site_properties=input_structure.site_properties,
        labels=input_structure.labels,
        properties=input_structure.properties,
    )


def normalize_coordinate_by_structure(input_structure, target_structure):
    input_frac_coord = input_structure.frac_coords.copy()
    target_frac_coord = target_structure.frac_coords.copy()
    
    for idx, i in enumerate(input_frac_coord):
        input_site = i
        target_site = target_frac_coord[idx]

        for j in range(3):
            while abs(input_site[j]+1-target_site[j]) < abs(input_site[j]-target_site[j]):
                input_site[j] += 1
            while abs(input_site[j]-1-target_site[j]) < abs(input_site[j]-target_site[j]):
                input_site[j] -= 1
    
    return Structure(
        lattice=input_structure.lattice,
        species=input_structure.species,
        coords=input_frac_coord,
        charge=input_structure.charge,
        validate_proximity=False,
        to_unit_cell=False,
        coords_are_cartesian=False,
        site_properties=input_structure.site_properties,
        labels=input_structure.labels,
        properties=input_structure.properties,
    )


def get_vacancy_diffusion_ini_fin(structure, idx_ini_0, idx_fin_0):
    structure_ini = structure.copy(properties=structure.properties, site_properties=structure.site_properties)
    structure_fin = structure.copy(properties=structure.properties, site_properties=structure.site_properties)
    
    for i in [structure_ini, structure_fin]:
        site_ini = i[idx_ini_0]
        site_fin = i[idx_fin_0]
        
        i.remove_sites([idx_ini_0, idx_fin_0])
        i.insert(
            idx=0,
            species=site_fin.species,
            coords=site_fin.frac_coords,
            coords_are_cartesian=False,
            validate_proximity=False,
            properties=site_fin.properties,
            label=site_fin.label,
        )
        i.insert(
            idx=0,
            species=site_ini.species,
            coords=site_ini.frac_coords,
            coords_are_cartesian=False,
            validate_proximity=False,
            properties=site_ini.properties,
            label=site_ini.label,
        )
    
    structure_ini.remove_sites([1])
    structure_fin.remove_sites([0])
    
    return structure_ini, structure_fin
