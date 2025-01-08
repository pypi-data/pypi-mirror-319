def get_average_distance(xdatcar, idx_atom_i, idx_atom_j, idx_start, idx_end, jimage=None, idx_step=1):
    if jimage == None:
        jimage = [None for i in range(len(idx_atom_i))]
    
    if not(len(idx_atom_i) == len(idx_atom_j) == len(jimage)):
        raise ValueError(
            'get_average_distance: not(len(idx_atom_i) == len(idx_atom_j) == len(jimage))'
        )
    
    current_idx_configuration = xdatcar.idx_configuration_0
    
    xdatcar.rewind()
    while xdatcar.idx_configuration_0 != (idx_start-1):
        xdatcar.read_next_configuration()
    
    distance = [[] for i in range(len(idx_atom_i))]
    for i in range(idx_start, idx_end):
        xdatcar.read_next_configuration()
        
        if ((i-idx_start)%idx_step) == 0:
            for idx, ii, jj, kk in zip(range(len(idx_atom_i)), idx_atom_i, idx_atom_j, jimage):
                distance[idx].append(xdatcar.get_distance(ii, jj, kk))
    
    xdatcar.seek(current_idx_configuration)
    
    average_distance = [sum(i)/len(i) for i in distance]
    return average_distance
