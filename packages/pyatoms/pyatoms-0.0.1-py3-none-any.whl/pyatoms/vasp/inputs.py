import itertools
from os.path import join

from pymatgen.core.structure import Structure
from pymatgen.io.vasp.inputs import Kpoints, Potcar, PotcarSingle

from pyatoms.utils.file import cp_r_atomic, rm_fr_atomic


def copy_vasp_input(src, dst, input=['INCAR', 'KPOINTS', 'POTCAR', 'submit.sh'], sort_incar_tag=True):
    if src == '':
        return
    
    if 'INCAR' not in input:
        sort_incar_tag = False

    if sort_incar_tag:
        input.remove('INCAR')
    
    for i in input:
        cp_r_atomic(join(src, i), join(dst, i))
    
    if sort_incar_tag:
        incar = INCAR()
        incar.read_from_file(join(src, 'INCAR'))
        incar.write(join(dst, 'INCAR'))


class KPOINTS:
    def __init__(self):
        self.kpts = None
    
    def set_kpts_according_to_user(self, user_defined_value):
        self.kpts = user_defined_value
    
    def write(self, path_saving):
        if self.kpts == None:
            print('vasp_utils.KPOINTS.write: ERROR!!! self.kpts == None, EXIT!')
            exit()
            
        Kpoints.gamma_automatic(kpts=self.kpts).write_file(join(path_saving))


class POTCAR:
    def __init__(self, recommended_potcar=None):
        if recommended_potcar == None:
            self.recommended_potcar = {
                'H'  : {'POTCAR' : 'H',     'ENMAX' : 250, 'VALANCY' : 1}, 
                'He' : {'POTCAR' : 'He',    'ENMAX' : 479, 'VALANCY' : 2}, 
                'Li' : {'POTCAR' : 'Li_sv', 'ENMAX' : 499, 'VALANCY' : 3}, 
                'Be' : {'POTCAR' : 'Be',    'ENMAX' : 248, 'VALANCY' : 2}, 
                'B'  : {'POTCAR' : 'B',     'ENMAX' : 319, 'VALANCY' : 3}, 
                'C'  : {'POTCAR' : 'C',     'ENMAX' : 400, 'VALANCY' : 4}, 
                'N'  : {'POTCAR' : 'N',     'ENMAX' : 400, 'VALANCY' : 5}, 
                'O'  : {'POTCAR' : 'O',     'ENMAX' : 400, 'VALANCY' : 6}, 
                'F'  : {'POTCAR' : 'F',     'ENMAX' : 400, 'VALANCY' : 7}, 
                'Ne' : {'POTCAR' : 'Ne',    'ENMAX' : 344, 'VALANCY' : 8}, 
                'Na' : {'POTCAR' : 'Na_pv', 'ENMAX' : 260, 'VALANCY' : 7}, 
                'Mg' : {'POTCAR' : 'Mg',    'ENMAX' : 200, 'VALANCY' : 2}, 
                'Al' : {'POTCAR' : 'Al',    'ENMAX' : 240, 'VALANCY' : 3}, 
                'Si' : {'POTCAR' : 'Si',    'ENMAX' : 245, 'VALANCY' : 4}, 
                'P'  : {'POTCAR' : 'P',     'ENMAX' : 255, 'VALANCY' : 5}, 
                'S'  : {'POTCAR' : 'S',     'ENMAX' : 259, 'VALANCY' : 6}, 
                'Cl' : {'POTCAR' : 'Cl',    'ENMAX' : 262, 'VALANCY' : 7}, 
                'Ar' : {'POTCAR' : 'Ar',    'ENMAX' : 266, 'VALANCY' : 8}, 
                'K'  : {'POTCAR' : 'K_sv',  'ENMAX' : 259, 'VALANCY' : 9}, 
                'Ca' : {'POTCAR' : 'Ca_sv', 'ENMAX' : 267, 'VALANCY' : 10}, 
                'Sc' : {'POTCAR' : 'Sc_sv', 'ENMAX' : 223, 'VALANCY' : 11}, 
                'Ti' : {'POTCAR' : 'Ti_sv', 'ENMAX' : 275, 'VALANCY' : 12}, 
                'V'  : {'POTCAR' : 'V_sv',  'ENMAX' : 264, 'VALANCY' : 13}, 
                'Cr' : {'POTCAR' : 'Cr_pv', 'ENMAX' : 266, 'VALANCY' : 12}, 
                'Mn' : {'POTCAR' : 'Mn_pv', 'ENMAX' : 270, 'VALANCY' : 13}, 
                'Fe' : {'POTCAR' : 'Fe',    'ENMAX' : 268, 'VALANCY' : 8}, 
                'Co' : {'POTCAR' : 'Co',    'ENMAX' : 268, 'VALANCY' : 9}, 
                'Ni' : {'POTCAR' : 'Ni',    'ENMAX' : 270, 'VALANCY' : 10}, 
                'Cu' : {'POTCAR' : 'Cu',    'ENMAX' : 295, 'VALANCY' : 11}, 
                'Zn' : {'POTCAR' : 'Zn',    'ENMAX' : 277, 'VALANCY' : 12}, 
                'Ga' : {'POTCAR' : 'Ga_d',  'ENMAX' : 283, 'VALANCY' : 13}, 
                'Ge' : {'POTCAR' : 'Ge_d',  'ENMAX' : 310, 'VALANCY' : 14}, 
                'As' : {'POTCAR' : 'As',    'ENMAX' : 209, 'VALANCY' : 5}, 
                'Se' : {'POTCAR' : 'Se',    'ENMAX' : 212, 'VALANCY' : 6}, 
                'Br' : {'POTCAR' : 'Br',    'ENMAX' : 216, 'VALANCY' : 7}, 
                'Kr' : {'POTCAR' : 'Kr',    'ENMAX' : 185, 'VALANCY' : 8}, 
                'Rb' : {'POTCAR' : 'Rb_sv', 'ENMAX' : 220, 'VALANCY' : 9}, 
                'Sr' : {'POTCAR' : 'Sr_sv', 'ENMAX' : 229, 'VALANCY' : 10}, 
                'Y'  : {'POTCAR' : 'Y_sv',  'ENMAX' : 203, 'VALANCY' : 11}, 
                'Zr' : {'POTCAR' : 'Zr_sv', 'ENMAX' : 230, 'VALANCY' : 12}, 
                'Nb' : {'POTCAR' : 'Nb_sv', 'ENMAX' : 293, 'VALANCY' : 13}, 
                'Mo' : {'POTCAR' : 'Mo_sv', 'ENMAX' : 243, 'VALANCY' : 14}, 
                'Tc' : {'POTCAR' : 'Tc_pv', 'ENMAX' : 264, 'VALANCY' : 13}, 
                'Ru' : {'POTCAR' : 'Ru_pv', 'ENMAX' : 240, 'VALANCY' : 14}, 
                'Rh' : {'POTCAR' : 'Rh_pv', 'ENMAX' : 247, 'VALANCY' : 15}, 
                'Pd' : {'POTCAR' : 'Pd',    'ENMAX' : 251, 'VALANCY' : 10}, 
                'Ag' : {'POTCAR' : 'Ag',    'ENMAX' : 250, 'VALANCY' : 11}, 
                'Cd' : {'POTCAR' : 'Cd',    'ENMAX' : 274, 'VALANCY' : 12}, 
                'In' : {'POTCAR' : 'In_d',  'ENMAX' : 239, 'VALANCY' : 13}, 
                'Sn' : {'POTCAR' : 'Sn_d',  'ENMAX' : 241, 'VALANCY' : 14}, 
                'Sb' : {'POTCAR' : 'Sb',    'ENMAX' : 172, 'VALANCY' : 5}, 
                'Te' : {'POTCAR' : 'Te',    'ENMAX' : 175, 'VALANCY' : 6}, 
                'I'  : {'POTCAR' : 'I',     'ENMAX' : 176, 'VALANCY' : 7}, 
                'Xe' : {'POTCAR' : 'Xe',    'ENMAX' : 153, 'VALANCY' : 8}, 
                'Cs' : {'POTCAR' : 'Cs_sv', 'ENMAX' : 220, 'VALANCY' : 9}, 
                'Ba' : {'POTCAR' : 'Ba_sv', 'ENMAX' : 187, 'VALANCY' : 10}, 
                'La' : {'POTCAR' : 'La',    'ENMAX' : 219, 'VALANCY' : 11}, 
                'Ce' : {'POTCAR' : 'Ce',    'ENMAX' : 273, 'VALANCY' : 12}, 
                'Pr' : {'POTCAR' : 'Pr_3',  'ENMAX' : 182, 'VALANCY' : 11}, 
                'Nd' : {'POTCAR' : 'Nd_3',  'ENMAX' : 183, 'VALANCY' : 11}, 
                'Pm' : {'POTCAR' : 'Pm_3',  'ENMAX' : 177, 'VALANCY' : 11}, 
                'Sm' : {'POTCAR' : 'Sm_3',  'ENMAX' : 177, 'VALANCY' : 11}, 
                'Eu' : {'POTCAR' : 'Eu_2',  'ENMAX' : 99,  'VALANCY' : 8}, 
                'Gd' : {'POTCAR' : 'Gd_3',  'ENMAX' : 154, 'VALANCY' : 9}, 
                'Tb' : {'POTCAR' : 'Tb_3',  'ENMAX' : 156, 'VALANCY' : 9}, 
                'Dy' : {'POTCAR' : 'Dy_3',  'ENMAX' : 156, 'VALANCY' : 9}, 
                'Ho' : {'POTCAR' : 'Ho_3',  'ENMAX' : 154, 'VALANCY' : 9}, 
                'Er' : {'POTCAR' : 'Er_3',  'ENMAX' : 155, 'VALANCY' : 9}, 
                'Tm' : {'POTCAR' : 'Tm_3',  'ENMAX' : 149, 'VALANCY' : 9}, 
                'Yb' : {'POTCAR' : 'Yb_2',  'ENMAX' : 113, 'VALANCY' : 8}, 
                'Lu' : {'POTCAR' : 'Lu_3',  'ENMAX' : 155, 'VALANCY' : 9}, 
                'Hf' : {'POTCAR' : 'Hf_pv', 'ENMAX' : 220, 'VALANCY' : 10}, 
                'Ta' : {'POTCAR' : 'Ta_pv', 'ENMAX' : 224, 'VALANCY' : 11}, 
                'W'  : {'POTCAR' : 'W_sv',  'ENMAX' : 223, 'VALANCY' : 14}, 
                'Re' : {'POTCAR' : 'Re',    'ENMAX' : 226, 'VALANCY' : 7}, 
                'Os' : {'POTCAR' : 'Os',    'ENMAX' : 228, 'VALANCY' : 8}, 
                'Ir' : {'POTCAR' : 'Ir',    'ENMAX' : 211, 'VALANCY' : 9}, 
                'Pt' : {'POTCAR' : 'Pt',    'ENMAX' : 230, 'VALANCY' : 10}, 
                'Au' : {'POTCAR' : 'Au',    'ENMAX' : 230, 'VALANCY' : 11}, 
                'Hg' : {'POTCAR' : 'Hg',    'ENMAX' : 233, 'VALANCY' : 12}, 
                'Tl' : {'POTCAR' : 'Tl_d',  'ENMAX' : 237, 'VALANCY' : 13}, 
                'Pb' : {'POTCAR' : 'Pb_d',  'ENMAX' : 238, 'VALANCY' : 14}, 
                'Bi' : {'POTCAR' : 'Bi_d',  'ENMAX' : 243, 'VALANCY' : 15}, 
                'Po' : {'POTCAR' : 'Po_d',  'ENMAX' : 265, 'VALANCY' : 16}, 
                'At' : {'POTCAR' : 'At',    'ENMAX' : 161, 'VALANCY' : 7}, 
                'Rn' : {'POTCAR' : 'Rn',    'ENMAX' : 151, 'VALANCY' : 8}, 
                'Fr' : {'POTCAR' : 'Fr_sv', 'ENMAX' : 215, 'VALANCY' : 9}, 
                'Ra' : {'POTCAR' : 'Ra_sv', 'ENMAX' : 237, 'VALANCY' : 10}, 
                'Ac' : {'POTCAR' : 'Ac',    'ENMAX' : 172, 'VALANCY' : 11}, 
                'Th' : {'POTCAR' : 'Th',    'ENMAX' : 247, 'VALANCY' : 12}, 
                'Pa' : {'POTCAR' : 'Pa',    'ENMAX' : 252, 'VALANCY' : 13}, 
                'U'  : {'POTCAR' : 'U',     'ENMAX' : 253, 'VALANCY' : 14}, 
                'Np' : {'POTCAR' : 'Np',    'ENMAX' : 254, 'VALANCY' : 15}, 
                'Pu' : {'POTCAR' : 'Pu',    'ENMAX' : 254, 'VALANCY' : 16}, 
                'Am' : {'POTCAR' : 'Am',    'ENMAX' : 256, 'VALANCY' : 17}, 
                'Cm' : {'POTCAR' : 'Cm',    'ENMAX' : 258, 'VALANCY' : 18}, 
            }
        else:
            self.recommended_potcar = recommended_potcar
        
        self.element = None
    
    def set_element_according_to_poscar(self, path_poscar):
        poscar = POSCAR()
        poscar.read_from_file(join(path_poscar))
        self.element = poscar.get_element_including_duplicated()
    
    def set_element_according_to_user(self, user_defined_value):
        self.element = user_defined_value
    
    def get_data(self, key):
        data = []
        for i in self.element:
            symbol = self.recommended_potcar[i]['POTCAR']
            data.append(PotcarSingle.from_symbol_and_functional(symbol, 'PBE_54').keywords[key])
        
        return data
    
    def write(self, path_saving):
        if self.element == None:
            print('vasp_utils.POTCAR.write: ERROR!!! self.element == None, EXIT!')
            exit()
        
        symbols = [self.recommended_potcar[i]['POTCAR'] for i in self.element]
        Potcar(symbols=symbols, functional='PBE_54').write_file(join(path_saving))


class INCAR:
    """
    use_incar_template
        type_job:
            'relax'
            'scf'
            'cineb'
    set_how_to_start:
        method:
            'start_from_scratch'
            'continue_from_WAVECAR'
            'continue_from_WAVECAR_and_CHGCAR'
            'continue_from_CHGCAR_for_nonscf'
    set_max_step:
        method:
            'convergence_first'
            'high_throughput'
    set_magnetic_moment:
        method:
            'off'
            'according_to_poscar'
            'user_defined_value'
    set_ldau:
        method:
            'off'
            'according_to_poscar'
    """
    def __init__(self, order=None, magmom=None):
        self.incar_content = {'SYSTEM' : 'material'}
        
        if order != None:
            self.order = order
        else:
            self.order = [
                'SYSTEM', 
                '', 
                'ISTART', 
                'ICHARG', 
                '', 
                'IBRION', 
                'ALGO', 
                'IALGO', 
                'ISIF', 
                '', 
                'NSW', 
                'NELM', 
                'NELMIN', 
                '', 
                'ISMEAR', 
                'SIGMA', 
                '', 
                'PREC', 
                'ENCUT', 
                'EDIFF', 
                'EDIFFG', 
                '', 
                'NELECT', 
                '', 
                'ISPIN', 
                'MAGMOM', 
                'LASPH', 
                'GGA_COMPAT', 
                '', 
                'LDAU', 
                'LDATYPE', 
                'LDAUL', 
                'LDAUU', 
                'LDAUJ', 
                '', 
                'IVDW', 
                '', 
                'NEDOS', 
                '', 
                'POTIM', 
                '', 
                'ADDGRID', 
                '', 
                'NGX', 
                'NGY', 
                'NGZ', 
                '', 
                'LMAXMIX', 
                '', 
                'LREAL', 
                '', 
                'ISYM', 
                'SYMPREC',                 
                '', 
                'LORBIT', 
                'LWAVE', 
                'LCHARG', 
                '', 
                'KPAR', 
                'NCORE', 
                '', 
                'ICHAIN', 
                'IMAGES', 
                'SPRING', 
                'LCLIMB', 
                '', 
                'IOPT', 
                'MAXMOVE', 
                'TIMESTEP', 
                '', 
                'MDALGO', 
                'SMASS', 
                'TEBEG', 
                'TEEND', 
                '', 
                'IOPTCELL', 
            ]
        
        if magmom != None:
            self.magmom = magmom
        else:
            self.magmom = {
                'H' : 0.0, 
                'He' : 0.0, 
                'Li' : 0.0, 
                'Be' : 0.0, 
                'B' : 0.0, 
                'C' : 0.0, 
                'N' : 0.0, 
                'O' : 0.0, 
                'F' : 0.0, 
                'Ne' : 0.0, 
                'Na' : 0.0, 
                'Mg' : 0.0, 
                'Al' : 0.0, 
                'Si' : 0.0, 
                'P' : 0.0, 
                'S' : 0.0, 
                'Cl' : 0.0, 
                'Ar' : 0.0, 
                'K' : 0.0, 
                'Ca' : 0.0, 
                'Sc' : 1.2, 
                'Ti' : 2.4, 
                'V' : 3.6, 
                'Cr' : 6.0, 
                'Mn' : 6.0, 
                'Fe' : 4.8, 
                'Co' : 3.6, 
                'Ni' : 2.4, 
                'Cu' : 1.0, 
                'Zn' : 0.0, 
                'Ga' : 0.0, 
                'Ge' : 0.0, 
                'As' : 0.0, 
                'Se' : 0.0, 
                'Br' : 0.0, 
                'Kr' : 0.0, 
                'Rb' : 0.0, 
                'Sr' : 0.0, 
                'Y' : 1.2, 
                'Zr' : 2.4, 
                'Nb' : 4.8, 
                'Mo' : 6.0, 
                'Tc' : 6.0, 
                'Ru' : 3.6, 
                'Rh' : 2.4, 
                'Pd' : 1.0, 
                'Ag' : 1.0, 
                'Cd' : 0.0, 
                'In' : 0.0, 
                'Sn' : 0.0, 
                'Sb' : 0.0, 
                'Te' : 0.0, 
                'I' : 0.0, 
                'Xe' : 0.0, 
                'Cs' : 0.0, 
                'Ba' : 0.0, 
                'La' : 1.2, 
                'Ce' : None, 
                'Pr' : None, 
                'Nd' : None, 
                'Pm' : None, 
                'Sm' : None, 
                'Eu' : None, 
                'Gd' : None, 
                'Tb' : None, 
                'Dy' : None, 
                'Ho' : None, 
                'Er' : None, 
                'Tm' : None, 
                'Yb' : None, 
                'Lu' : None, 
                'Hf' : 2.4, 
                'Ta' : 3.6, 
                'W' : 4.8, 
                'Re' : 6.0, 
                'Os' : 4.8, 
                'Ir' : 3.6, 
                'Pt' : 1.2, 
                'Au' : 1.0, 
                'Hg' : 0.0, 
                'Tl' : 0.0, 
                'Pb' : 0.0, 
                'Bi' : 0.0, 
                'Po' : 0.0, 
                'At' : 0.0, 
                'Rn' : 0.0, 
                'Fr' : 0.0, 
                'Ra' : 0.0, 
                'Ac' : None, 
                'Th' : None, 
                'Pa' : None, 
                'U' : None, 
                'Np' : None, 
                'Pu' : None, 
                'Am' : None, 
                'Cm' : None, 
                'Bk' : None, 
                'Cf' : None, 
                'Es' : None, 
                'Fm' : None, 
                'Md' : None, 
                'No' : None, 
                'Lr' : None, 
                'Rf' : None, 
                'Db' : None, 
                'Sg' : None, 
                'Bh' : None, 
                'Hs' : None, 
                'Mt' : None, 
                'Ds' : None, 
                'Rg' : None, 
                'Cn' : None, 
                'Nh' : None, 
                'Fl' : None, 
                'Mc' : None, 
                'Lv' : None, 
                'Ts' : None, 
                'Og' : None, 
            }
    
    def read_from_file(self, path_incar):
        # please mind, if this method is used to read the contents of the INCAR, then all values in 
        # the key-value pairs will be in the form of str
        self.incar_content = {}
        
        with open(join(path_incar)) as f:
            for i in f:
                if i == '\n':
                    continue
                else:
                    key = i.split(sep='=')[0].strip()
                    value = i.split(sep='=')[1].strip()
                    self.incar_content[key] = value
    
    def use_incar_template(self, type_job):
        self.incar_content.clear()
        self.incar_content['SYSTEM'] = 'material'
        
        if type_job == 'relax':
            # mind: the following settings are designed for routine material study, aimed at 
            # ensuring accuracy and achieving convergence, without considering the conservation of 
            # resources
            
            # a fresh start
            # "begin from scratch". Initialize the orbitals according to the flag INIWAV
            self.incar_content['ISTART'] = 0
            # take superposition of atomic charge densities
            self.incar_content['ICHARG'] = 2
            
            # ion update: relaxation, conjugate gradient algorithm
            self.incar_content['IBRION'] = 2
            # electron update: blocked-Davidson-iteration scheme
            self.incar_content['ALGO'] = 'Normal'
            # degrees-of-freedom: update ion positions, cell shape, and cell volume
            self.incar_content['ISIF'] = 3
            
            # max ionic step
            self.incar_content['NSW'] = 2000
            # max electronic step
            self.incar_content['NELM'] = 500
            # min electronic step
            self.incar_content['NELMIN'] = 4
            
            # smearing
            self.incar_content['ISMEAR'] = 0
            self.incar_content['SIGMA'] = 0.03
            
            # precision
            # global precision mode
            self.incar_content['PREC'] = 'Accurate'
            # energy cutoff for the plane-wave basis set
            self.incar_content['ENCUT'] = 520
            # break condition for the electronic SC-loop
            self.incar_content['EDIFF'] = 1E-07
            # break condition for the ionic relaxation loop
            self.incar_content['EDIFFG'] = -1E-03
            
            # always turn on vdW, since it is really cheap
            self.incar_content['IVDW'] = 12
            
            # set LORBIT=11 to get more info about local properties
            # mind: this projection is cheap but write a lot files on the disk
            self.incar_content['LORBIT'] = 11
            
            # consider symmetry to simply the calculation
            self.incar_content['ISYM'] = 2
            
            # for large system, use LREAL=Auto
            self.incar_content['LREAL'] = 'Auto'
            
            # do not save the wavefunctions or the charge density
            self.incar_content['LWAVE'] = '.FALSE.'
            self.incar_content['LCHARG'] = '.FALSE.'
            
            # parallel parameters which should be set according to both the system and the HPC
            # correct settings can greatly speed up the calculations
            # the following is the worst setting, and should be modified manually
            # number of k-points that are to be treated in parallel
            self.incar_content['KPAR'] = 1
            # number of compute cores that work on an individual orbital
            self.incar_content['NCORE'] = 1
            
        elif type_job == 'scf':
            self.incar_content['ISTART'] = 0
            self.incar_content['ICHARG'] = 2
            
            # ion update: no update
            self.incar_content['IBRION'] = -1
            self.incar_content['ALGO'] = 'Normal'
            # for a simple scf calculation, the ion positions, cell shape, and cell volume will not change
            # self.incar_content['ISIF'] = 3
            
            # scf calculation do not involve ionic steps
            self.incar_content['NSW'] = 0
            self.incar_content['NELM'] = 500
            self.incar_content['NELMIN'] = 4
            
            self.incar_content['ISMEAR'] = 0
            self.incar_content['SIGMA'] = 0.03
            
            self.incar_content['PREC'] = 'Accurate'
            self.incar_content['ENCUT'] = 520
            # scf is typically conducted to obtain accurate electronic structure, thus requiring sufficient electronic convergence
            self.incar_content['EDIFF'] = 1E-08
            # scf calculation do not involve ionic steps
            # self.incar_content['EDIFFG'] = -1E-03
            
            self.incar_content['IVDW'] = 12
            
            self.incar_content['LORBIT'] = 11
            
            self.incar_content['ISYM'] = 2
            
            self.incar_content['LREAL'] = 'Auto'
            
            self.incar_content['LWAVE'] = '.FALSE.'
            self.incar_content['LCHARG'] = '.FALSE.'
            
            self.incar_content['KPAR'] = 1
            self.incar_content['NCORE'] = 1
            
        elif type_job == 'cineb':
            self.incar_content['ISTART'] = 0
            self.incar_content['ICHARG'] = 2
            
            # set IBRION=3 and POTIM=0, to disable the built in optimizers
            self.incar_content['IBRION'] = 3
            self.incar_content['ALGO'] = 'Normal'
            # most cineb calculations fix the cell
            self.incar_content['ISIF'] = 2
            
            self.incar_content['NSW'] = 2000
            self.incar_content['NELM'] = 500
            self.incar_content['NELMIN'] = 4
            
            self.incar_content['ISMEAR'] = 0
            self.incar_content['SIGMA'] = 0.03
            
            self.incar_content['PREC'] = 'Accurate'
            self.incar_content['ENCUT'] = 520
            # changes in conjunction with EDIFFG (by a factor of 1E-04)
            self.incar_content['EDIFF'] = 1E-05
            # cineb generally have difficulty converging, so it's advisable to first aim for a relatively rough standard
            self.incar_content['EDIFFG'] = -1E-01
            
            self.incar_content['IVDW'] = 12
            
            self.incar_content['LORBIT'] = 11
            
            self.incar_content['ISYM'] = 2
            
            self.incar_content['LREAL'] = 'Auto'
            
            self.incar_content['LWAVE'] = '.FALSE.'
            self.incar_content['LCHARG'] = '.FALSE.'
            
            self.incar_content['KPAR'] = 1
            self.incar_content['NCORE'] = 1
            
            # cineb related tags
            # set IBRION=3 and POTIM=0, to disable the built in optimizers
            self.incar_content['POTIM'] = 0
            # ICHAIN=0: nudged elastic band
            self.incar_content['ICHAIN'] = 0
            # number of neb images between the fixed endpoints
            self.incar_content['IMAGES'] = 5
            # the spring constant
            self.incar_content['SPRING'] = 0
            # to use the climbing image, set LCLIMB = .TRUE.
            self.incar_content['LCLIMB'] = 0
            # optimizer: LBFGS = Limited-memory Broyden-Fletcher-Goldfarb-Shanno
            self.incar_content['IOPT'] = 1
    
    def set_value(self, key, value):
        self.incar_content[key] = value
    
    def get_value(self, key):
        return self.incar_content[key]
    
    def del_value(self, key):
        if key in self.incar_content:
            self.incar_content.pop(key)
    
    def set_how_to_start(self, method):
        if method == 'start_from_scratch':
            self.set_value('ISTART', 0)
            self.set_value('ICHARG', 2)
        elif method == 'continue_from_WAVECAR':
            self.set_value('ISTART', 1)
            self.set_value('ICHARG', 0)
        elif method == 'continue_from_WAVECAR_and_CHGCAR':
            self.set_value('ISTART', 1)
            self.set_value('ICHARG', 1)
        elif method == 'continue_from_CHGCAR_for_nonscf':
            self.set_value('ISTART', 0)
            self.set_value('ICHARG', 11)
    
    def set_max_step(self, method):
        if method == 'convergence_first':
            if self.get_value('NSW') != 0:
                self.set_value('NSW', 2000)
            self.set_value('NELM', 500)
        elif method == 'high_throughput':
            if self.get_value('NSW') != 0:
                self.set_value('NSW', 300)
            self.set_value('NELM', 150)
    
    def set_magnetic_moment(self, method, path_poscar=None, user_defined_value=None):
        if method == 'off':
            for i in ['ISPIN', 'MAGMOM', 'LASPH', 'GGA_COMPAT']:
                self.del_value(i)
        elif method == 'according_to_poscar':
            if path_poscar == None:
                print('vasp_utils.INCAR.set_magnetic_moment: ERROR!!! path_poscar == None, EXIT!')
                exit()
            else:
                poscar = Structure.from_file(join(path_poscar))
                
                recommended_value=[]
                for i in poscar:
                    recommended = self.magmom[i.species_string]
                    if recommended == None:
                        recommended_value.append(1.0)
                    else:
                        recommended_value.append(recommended)
                
                recommended_value_string = ''
                for i in recommended_value:
                    recommended_value_string += '%.2f ' % (i)
                
                self.set_value('MAGMOM', recommended_value_string)
        elif method == 'user_defined_value':
            if user_defined_value == None:
                print('vasp_utils.INCAR.set_magnetic_moment: ERROR!!! user_defined_value == None, EXIT!')
                exit()
            else:
                self.set_value('MAGMOM', user_defined_value)
        
        if method != 'off':
            self.set_value('ISPIN', 2)
            self.set_value('LASPH', '.TRUE.')
            self.set_value('GGA_COMPAT', '.FALSE.')
    
    def set_ldau(self, method, path_poscar=None, u_value=None):
        if method == 'off':
            for i in ['LDAU', 'LDATYPE', 'LDAUL', 'LDAUU', 'LDAUJ']:
                self.del_value(i)
        elif method == 'according_to_poscar':
            if (path_poscar==None) or (u_value==None):
                print('vasp_utils.INCAR.set_ldau: ERROR!!! (path_poscar==None) or (u_value==None), EXIT!')
                exit()
            
            poscar = POSCAR()
            poscar.read_from_file(join(path_poscar))
            
            element = poscar.get_element_including_duplicated()
            
            ldaul = []
            ldauu = []
            ldauj = []
            for i in element:
                if i in u_value:
                    ldaul.append(u_value[i]['LDAUL'])
                    ldauu.append(u_value[i]['LDAUU'])
                    ldauj.append(u_value[i]['LDAUJ'])
                else:
                    ldaul.append(-1)
                    ldauu.append(0.0)
                    ldauj.append(0.0)
            
            ldaul_string = ''
            ldauu_string = ''
            ldauj_string = ''
            for i in ldaul:
                ldaul_string += '%d ' % (i)
            for i in ldauu:
                ldauu_string += '%.2f ' % (i)
            for i in ldauj:
                ldauj_string += '%.2f ' % (i)
            
            self.set_value('LDAUL', ldaul_string)
            self.set_value('LDAUU', ldauu_string)
            self.set_value('LDAUJ', ldauj_string)
        
        if method != 'off':
            self.set_value('LDAU', '.TRUE.')
            self.set_value('LDATYPE', '2')
            
    def set_kpar_and_ncore(self, server, with_gpu, kpar_and_ncore):
        if server not in kpar_and_ncore:
            print('vasp_utils.INCAR.set_kpar_and_ncore: ERROR!!! server not in kpar_and_ncore, EXIT!')
            exit()
        else:
            self.set_value('KPAR', str(kpar_and_ncore[server][with_gpu]['KPAR']))
            self.set_value('NCORE', str(kpar_and_ncore[server][with_gpu]['NCORE']))
    
    def write(self, path_saving):
        for i in self.incar_content.keys():
            if i not in self.order:
                print('vasp_utils.INCAR.write_incar: ERROR!!! i not in self.order, %s, please update the self.order list. EXIT!' % (i))
                exit()
        
        rm_fr_atomic(path_saving)
        
        with open(join(path_saving), mode='w') as f:
            last_line = None
            for i in self.order:
                if (i == '') and (last_line != ''):
                    f.write('\n')
                    last_line = ''
                elif i in self.incar_content:
                    tag = '%s=%s\n' % (i, self.incar_content[i])
                    f.write(tag)
                    last_line = tag


class POSCAR:
    def __init__(self):
        self.poscar = None
    
    def read_from_file(self, path_poscar):
        self.poscar = Structure.from_file(join(path_poscar))
    
    def get_element_including_duplicated(self):
        if self.poscar == None:
            print('vasp_utils.POSCAR.get_element_including_duplicated: ERROR!!! self.poscar == None, EXIT!')
            exit()
        
        element = []
        for i, j in itertools.groupby([k.species_string for k in self.poscar]):
            element.append(i)
        
        return element
