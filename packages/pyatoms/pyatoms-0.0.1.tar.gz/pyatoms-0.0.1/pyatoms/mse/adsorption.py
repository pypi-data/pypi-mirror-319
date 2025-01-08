import numpy as np


def adsorb_molecule(slab, mol, neighbour_idx, z, mol_ref_point):
    """
    z:
        'method':
            'above_center'
            'above_slab'
            'user_defined_frac_coord'
        'distance' ('above_center')
        'distance' ('above_slab')
        'frac_coord' ('user_defined_frac_coord')
    mol_ref_point:
        'method':
            'center'
            'top_atom'
            'bottom_atom'
            'top_center'
            'bottom_center'
            'user_defined_atom'
        'atom_idx' ('user_defined_atom')
    """
    slab = slab.copy(properties=slab.properties, site_properties=slab.site_properties)
    
    coord_sum = np.zeros(3)
    for i in neighbour_idx:
        coord_sum += slab[i].frac_coords
    
    center = coord_sum / len(neighbour_idx)
    
    position_on_slab = np.zeros(3)
    if z['method'] == 'above_center':
        position_on_slab[:2] = center[:2]
        position_on_slab[2] = center[2] + z['distance'] / slab.lattice.c
    elif z['method'] == 'above_slab':
        slab_top = -1.00E08
        for i in slab:
            if i.frac_coords[2] > slab_top:
                slab_top = i.frac_coords[2]
        
        position_on_slab[:2] = center[:2]
        position_on_slab[2] = slab_top + z['distance'] / slab.lattice.c
    elif z['method'] == 'user_defined_frac_coord':
        position_on_slab = z['frac_coord']
    else:
        raise ValueError(
            'adsorb_molecule: valid z[\'method\']: {\'above_center\', \'above_slab\', \'user_defined_frac_coord\', z[\'method\']: %s}' % (z['method'])
        )
    
    coord_sum = np.zeros(3)
    for i in mol:
        coord_sum += i.frac_coords
    
    center = coord_sum / len(mol)
    
    top_atom_coord = np.array([0.00, 0.00, -1.00E08])
    bottom_atom_coord = np.array([0.00, 0.00, 1.00E08])
    for i in mol:
        if i.frac_coords[2] > top_atom_coord[2]:
            top_atom_coord[:] = i.frac_coords[:]
        if i.frac_coords[2] < bottom_atom_coord[2]:
            bottom_atom_coord[:] = i.frac_coords[:]
    
    position_on_mol = np.zeros(3)
    if mol_ref_point['method'] == 'center':
        position_on_mol[:] = center[:]
    elif mol_ref_point['method'] == 'top_atom':
        position_on_mol[:] = top_atom_coord[:]
    elif mol_ref_point['method'] == 'bottom_atom':
        position_on_mol[:] = bottom_atom_coord[:]
    elif mol_ref_point['method'] == 'top_center':
        position_on_mol[:2] = center[:2]
        position_on_mol[2] = top_atom_coord[2]
    elif mol_ref_point['method'] == 'bottom_center':
        position_on_mol[:2] = center[:2]
        position_on_mol[2] = bottom_atom_coord[2]
    elif mol_ref_point['method'] == 'user_defined_atom':
        position_on_mol[:2] = mol[mol_ref_point['atom_idx']].frac_coords
    else:
        raise ValueError(
            'adsorb_molecule: valid mol_ref_point[\'method\']: {\'center\', \'top_atom\', \'bottom_atom\', \'top_center\', \'bottom_center\', \'user_defined_atom\', mol_ref_point[\'method\']: %s}' % (mol_ref_point['method'])
        )
    
    vector = position_on_slab - position_on_mol
    
    properties = {'selective_dynamics': [True, True, True]} if 'selective_dynamics' in slab.site_properties else None
    
    for i in mol:
        insert_idx = None
        for j in range(len(slab)):
            if slab[j].species_string == i.species_string:
                insert_idx = j
        if insert_idx == None:
            insert_idx = len(slab)
        else:
            insert_idx += 1
        
        slab.insert(insert_idx, i.species_string, i.frac_coords+vector, properties=properties)
    
    return slab


def adsorb_single_atom(slab, element, neighbour_idx, z):
    """
    z:
        'method':
            'above_center'
            'above_slab'
            'user_defined_frac_coord'
        'distance' ('above_center')
        'distance' ('above_slab')
        'frac_coord' ('user_defined_frac_coord')
    """
    slab = slab.copy(properties=slab.properties, site_properties=slab.site_properties)
    
    coord_sum = np.zeros(3)
    for i in neighbour_idx:
        coord_sum += slab[i].frac_coords
    
    center = coord_sum / len(neighbour_idx)
    
    insert_idx = None
    for i in range(len(slab)):
        if slab[i].species_string == element:
            insert_idx = i
    if insert_idx == None:
        insert_idx = len(slab)
    else:
        insert_idx += 1
    
    properties = {'selective_dynamics': [True, True, True]} if 'selective_dynamics' in slab.site_properties else None
    
    if z['method'] == 'above_center':
        center[2] += z['distance'] / slab.lattice.c
        
        slab.insert(insert_idx, element, center, properties=properties)
    elif z['method'] == 'above_slab':
        slab_top = -1.00E08
        for i in slab:
            if i.frac_coords[2] > slab_top:
                slab_top = i.frac_coords[2]
        
        center[2] = slab_top + z['distance'] / slab.lattice.c
        
        slab.insert(insert_idx, element, center, properties=properties)
    elif z['method'] == 'user_defined_frac_coord':
        slab.insert(insert_idx, element, z['frac_coord'], properties=properties)
    else:
        raise ValueError(
            'adsorb_single_atom: valid z[\'method\']: {\'above_center\', \'above_slab\', \'user_defined_frac_coord\', z[\'method\']: %s}' % (z['method'])
        )
    
    return slab
