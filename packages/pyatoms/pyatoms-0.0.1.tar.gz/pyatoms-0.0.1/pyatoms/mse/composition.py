from pymatgen.core.composition import Composition

from pyatoms.utils.mathlib import is_integer


def get_composition_str(comp_dict, element_order=None, omit_one=True, tol=1E-05, ndigits=4, sep=''):
    normal_str = r''
    
    if element_order == None:
        element_order = comp_dict.keys()
    
    for idx, i in enumerate(element_order):
        if omit_one and (is_integer(comp_dict[i]) and (round(comp_dict[i])==1)):
            normal_str += r'%s' % (i)
        else:
            normal_str += r'%s%d' % (i, round(comp_dict[i])) if is_integer(comp_dict[i]) else (r'%s%.'+str(ndigits)+r'f') % (i, round(comp_dict[i], ndigits))
        
        if idx != (len(element_order)-1):
            normal_str += sep
    
    return normal_str


def get_composition_latex_str(comp_dict, element_order=None, omit_one=True, tol=1E-05, ndigits=4, sep=''):
    latex_str = r''
    
    if element_order == None:
        element_order = comp_dict.keys()
    
    for idx, i in enumerate(element_order):
        if omit_one and (is_integer(comp_dict[i]) and (round(comp_dict[i])==1)):
            latex_str += r'%s' % (i)
        else:
            latex_str += r'%s$_{%d}$' % (i, round(comp_dict[i])) if is_integer(comp_dict[i]) else (r'%s$_{%.'+str(ndigits)+r'f}$') % (i, round(comp_dict[i], ndigits))
        
        if idx != (len(element_order)-1):
            latex_str += sep
    
    return latex_str


def get_composition_dict(comp, tol=1E-05):
    comp = Composition(comp)
    formula = comp.__str__().split()
    chemical_system = [i.symbol for i in comp.elements]
    
    comp_dict = {}
    for idx, item in enumerate(chemical_system):
        float_num = float(formula[idx].split(sep=item)[1])
        comp_dict[item] = round(float_num) if is_integer(float_num, tol) else float_num
    
    return comp_dict
