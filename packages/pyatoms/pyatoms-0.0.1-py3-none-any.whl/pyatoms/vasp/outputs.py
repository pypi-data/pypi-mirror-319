import os

from pymatgen.core.structure import Structure

from pyatoms.utils.bash import grep
from pyatoms.vasp.errors import OUTCARError, XDATCARError


class VaspOut:
    def __init__(self, path_vasp_out):
        self.path_vasp_out = path_vasp_out
    
    def reached_required_accuracy(self):
        return grep(' reached required accuracy - stopping structural energy minimisation', self.path_vasp_out) != ''


class XDATCAR:
    
    # Note: This should only be used for static XDATCAR files, i.e., XDATCAR 
    # files from stopped VASP runs
    
    # Unfortunately, this is really slow. We have to find a much more 
    # efficient way to implement this
    
    def __init__(self, path_xdatcar):
        if os.path.isfile(path_xdatcar) == False:
            raise ValueError(
                'XDATCAR.__init__: os.path.isfile(path_xdatcar) == False'
            )
        
        self.path_xdatcar = path_xdatcar
        
        try:
            self.xdatcar = open(path_xdatcar, mode='r')
            self.system = self.xdatcar.readline().strip()
            self.scaling_factor = float(self.xdatcar.readline().strip())
            self.lattice = []
            for i in range(3):
                self.lattice.append([float(j) for j in self.xdatcar.readline().split()])
            self.element = self.xdatcar.readline().split()
            self.num_atom = [int(i) for i in self.xdatcar.readline().split()]
            
            self.tot_num_atom = sum(self.num_atom)
            self.species = []
            for element, num_atom in zip(self.element, self.num_atom):
                self.species += [element for i in range(num_atom)]
        except:
            raise XDATCARError(
                'XDATCAR.__init__: Exceptions occured while reading the header of XDATCAR'
            )
        
        self.idx_configuration_0 = -1
        self.current_position = None
        self.current_structure = None
    
    def read_next_configuration(self):
        next_line = self.xdatcar.readline()
        
        if 'Direct configuration=' not in next_line:
            return False
        
        idx_configuration_1 = int(next_line.split()[2])
        assert (self.idx_configuration_0+1+1) == idx_configuration_1
        
        position = []
        for i in range(self.tot_num_atom):
            next_line = self.xdatcar.readline()
            
            if len(next_line.split()) != 3:
                return False
            
            try:
                position.append([float(j) for j in next_line.split()])
            except:
                raise XDATCARError(
                    'XDATCAR.read_next_configuration: Exceptions occured in position.append([float(j) for j in next_line.split()])'
                )
        
        self.idx_configuration_0 += 1
        self.current_position = position
        self.current_structure = Structure(self.lattice, self.species, self.current_position)
        
        return True
    
    def get_distance(self, idx_i, idx_j, jimage=None):
        return self.current_structure.get_distance(idx_i, idx_j, jimage)
    
    def rewind(self):
        self.xdatcar.seek(0)
        for i in range(7):
            self.xdatcar.readline()
        self.idx_configuration_0 = -1
        self.current_position = None
        self.current_structure = None
    
    def seek(self, idx_configuration_0):
        self.rewind()
        
        while self.idx_configuration_0 != idx_configuration_0:
            self.read_next_configuration()
    
    def get_num_configuration(self):
        current_idx = self.idx_configuration_0
        
        num_configuration = None
        while self.read_next_configuration():
            pass
        num_configuration = self.idx_configuration_0 + 1
        
        self.rewind()
        self.seek(current_idx)
        
        return num_configuration
    
    def close(self):
        self.xdatcar.close()


class OUTCAR:
    def __init__(self):
        self.path_outcar = None
    
    def set_path_outcar(self, path_outcar):
        try:
            file = open(path_outcar)
            file.close()
        except:
            pass
        else:
            self.path_outcar = path_outcar
    
    def get_ngxyz(self):
        ngxyz_line = grep('dimension x,y,z NGX =', self.path_outcar)
        
        if ngxyz_line == '':
            raise OUTCARError(
                'OUTCAR.get_ngxyz: ngxyz_line: \'\''
            )
        else:
            ngxyz_line = ngxyz_line.split()
            ngxyz = {
                'NGX' : int(ngxyz_line[4]), 
                'NGY' : int(ngxyz_line[7]), 
                'NGZ' : int(ngxyz_line[10]), 
            }
        
        return ngxyz
    
    def get_nelect(self):
        nelect_line = grep('total number of electrons', self.path_outcar)
        
        if nelect_line == '':
            raise OUTCARError(
                'OUTCAR.get_nelect: nelect_line: \'\''
            )
        else:
            nelect_line = nelect_line.split()
            nelect = int(float(nelect_line[2]))
        
        return nelect
    
    def get_energy_sigma0(self):
        energy_sigma0_line = grep('energy  without entropy=', self.path_outcar).splitlines()[-1]
        
        if energy_sigma0_line == '':
            raise OUTCARError(
                'OUTCAR.get_energy_sigma0: energy_sigma0_line: \'\''
            )
        else:
            energy_sigma0_line = energy_sigma0_line.split()
            energy_sigma0 = float(energy_sigma0_line[6])
        
        return energy_sigma0
