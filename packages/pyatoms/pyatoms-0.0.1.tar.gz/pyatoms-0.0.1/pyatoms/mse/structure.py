import math
from collections.abc import Iterator
from copy import deepcopy
from itertools import product
from typing import Union

import numpy as np
from numpy.testing import assert_allclose
from pymatgen.analysis.elasticity.strain import Deformation
from pymatgen.analysis.interfaces.coherent_interfaces import from_2d_to_3d, get_2d_transform
from pymatgen.analysis.interfaces.zsl import ZSLGenerator
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core.interface import Interface, label_termination
from pymatgen.core.structure import Structure
from pymatgen.core.surface import Slab as PymatgenSlab
from pymatgen.core.surface import SlabGenerator
from scipy.linalg import polar

from pyatoms.mse.composition import get_composition_dict
from pyatoms.utils.mathlib import calc_angle_between_two_vector


MAPPING_DIRECTION_TO_IDX = {
    'a': 0, 
    'b': 1, 
    'c': 2, 
}


def move_to_center(structure, direction=('a', 'b', 'c')):
    direction_idx = [MAPPING_DIRECTION_TO_IDX[i] for i in direction]
    
    center_frac_coord = calc_center(structure, direction)
    
    frac_coord = structure.frac_coords.copy()
    for idx, i in enumerate(direction_idx):
        frac_coord[:, i] += (0.5 - center_frac_coord[idx])
    
    return Structure(
        lattice=structure.lattice, 
        species=structure.species, 
        coords=frac_coord,
        site_properties=structure.site_properties, 
        properties=structure.properties,
    )


def calc_center(structure, direction=('a', 'b', 'c'), type_coord='frac'):
    direction_idx = [MAPPING_DIRECTION_TO_IDX[i] for i in direction]
    
    if type_coord == 'frac':
        return [structure.frac_coords[:, i].mean() for i in direction_idx]
    elif type_coord == 'cart':
        return [structure.cart_coords[:, i].mean() for i in direction_idx]
    else:
        raise ValueError(
            "materials_science_utils.calc_center: type_coord should be 'frac' or 'cart', however, type_coord == %s" % (type_coord)
        )


def calc_length(structure, direction=('a', 'b', 'c')):
    direction_idx = [MAPPING_DIRECTION_TO_IDX[i] for i in direction]
    
    return [(structure.frac_coords[:, i].max()-structure.frac_coords[:, i].min())*structure.lattice.abc[i] for i in direction_idx]


def cluster_to_ref_atom(structure, idx_ref_atom_0):
    frac_coord = structure.frac_coords
    frac_coord_ref_atom = structure[idx_ref_atom_0].frac_coords
    
    for i in frac_coord:
        for j in range(3):
            while abs(i[j]+1-frac_coord_ref_atom[j]) < abs(i[j]-frac_coord_ref_atom[j]):
                i[j] += 1
            while abs(i[j]-1-frac_coord_ref_atom[j]) < abs(i[j]-frac_coord_ref_atom[j]):
                i[j] -= 1
    
    structure = Structure(
        lattice=structure.lattice, 
        species=structure.species, 
        coords=frac_coord, 
        site_properties=structure.site_properties, 
        properties=structure.properties, 
    )
    
    return structure


class ModifiedCoherentInterfaceBuilder:
    '''
    Modified from pymatgen.analysis.interfaces.coherent_interfaces.CoherentInterfaceBuilder, 
    with the aim of better implementing the algorithm described in K. Wang, 
    J. Janek, D. Mollenhauer, Chem. Mater. 2024, 36, 5133-5141.
    '''
    
    def __init__(
        self,
        substrate_structure: Structure,
        film_structure: Structure,
        film_miller: tuple[int, int, int],
        substrate_miller: tuple[int, int, int],
        zslgen: Union[ZSLGenerator, None] = None,
        slab_substrate: Structure = None, 
        slab_film: Structure = None, 
        super_ouc_substrate: Structure = None, 
        super_ouc_film: Structure = None, 
    ):
        # Bulk structures
        self.substrate_structure = substrate_structure
        self.film_structure = film_structure
        self.film_miller = film_miller
        self.substrate_miller = substrate_miller
        self.zslgen = zslgen or ZSLGenerator(bidirectional=True)
        
        self.slab_substrate = slab_substrate
        self.slab_film = slab_film
        self.super_ouc_substrate = super_ouc_substrate
        self.super_ouc_film = super_ouc_film
        
        a, b, c = self.slab_substrate.lattice.matrix
        a_ouc, b_ouc, c_ouc = self.super_ouc_substrate.lattice.matrix
        assert_allclose(a, a_ouc)
        assert_allclose(b, b_ouc)
        assert_allclose(c/np.linalg.norm(c), c_ouc/np.linalg.norm(c_ouc))
        
        a, b, c = self.slab_film.lattice.matrix
        a_ouc, b_ouc, c_ouc = self.super_ouc_film.lattice.matrix
        assert_allclose(a, a_ouc)
        assert_allclose(b, b_ouc)
        assert_allclose(c/np.linalg.norm(c), c_ouc/np.linalg.norm(c_ouc))
        
        self._find_matches()
        self._find_terminations()

    def _find_matches(self) -> None:
        self.zsl_matches = []

        film_sg = SlabGenerator(
            self.film_structure,
            self.film_miller,
            min_slab_size=1,
            min_vacuum_size=3,
            in_unit_planes=True,
            center_slab=True,
            primitive=True,
            reorient_lattice=False,  # This is necessary to not screw up the lattice
        )

        sub_sg = SlabGenerator(
            self.substrate_structure,
            self.substrate_miller,
            min_slab_size=1,
            min_vacuum_size=3,
            in_unit_planes=True,
            center_slab=True,
            primitive=True,
            reorient_lattice=False,  # This is necessary to not screw up the lattice
        )

        film_slab = film_sg.get_slab(shift=0)
        sub_slab = sub_sg.get_slab(shift=0)

        film_vectors = film_slab.lattice.matrix
        substrate_vectors = sub_slab.lattice.matrix
        
        a, b, c = film_vectors
        a_, b_, c_ = self.slab_film.lattice.matrix
        assert_allclose(np.linalg.norm(a), np.linalg.norm(a_))
        assert_allclose(np.linalg.norm(b), np.linalg.norm(b_))
        
        a, b, c = substrate_vectors
        a_, b_, c_ = self.slab_substrate.lattice.matrix
        assert_allclose(np.linalg.norm(a), np.linalg.norm(a_))
        assert_allclose(np.linalg.norm(b), np.linalg.norm(b_))
        
        # Generate all possible interface matches
        self.zsl_matches = list(self.zslgen(self.slab_film.lattice.matrix[:2], self.slab_substrate.lattice.matrix[:2], lowest=False))

        for match in self.zsl_matches:
            xform = get_2d_transform(self.slab_film.lattice.matrix, match.film_vectors)
            strain, _rot = polar(xform)
            (
                assert_allclose(strain, np.round(strain), atol=1e-12),
                "Film lattice vectors changed during ZSL match, check your ZSL Generator parameters",
            )

            xform = get_2d_transform(self.slab_substrate.lattice.matrix, match.substrate_vectors)
            strain, _rot = polar(xform)
            (
                assert_allclose(strain, strain.astype(int), atol=1e-12),
                "Substrate lattice vectors changed during ZSL match, check your ZSL Generator parameters",
            )

    def _find_terminations(self):
        film_sg = SlabGenerator(
            self.film_structure,
            self.film_miller,
            min_slab_size=1,
            min_vacuum_size=3,
            in_unit_planes=True,
            center_slab=True,
            primitive=True,
            reorient_lattice=False,  # This is necessary to not screw up the lattice
        )

        sub_sg = SlabGenerator(
            self.substrate_structure,
            self.substrate_miller,
            min_slab_size=1,
            min_vacuum_size=3,
            in_unit_planes=True,
            center_slab=True,
            primitive=True,
            reorient_lattice=False,  # This is necessary to not screw up the lattice
        )

        film_slabs = film_sg.get_slabs()
        sub_slabs = sub_sg.get_slabs()

        film_shifts = [s.shift for s in film_slabs]
        film_terminations = [label_termination(s) for s in film_slabs]

        sub_shifts = [s.shift for s in sub_slabs]
        sub_terminations = [label_termination(s) for s in sub_slabs]

        self._terminations = {
            (film_label, sub_label): (film_shift, sub_shift)
            for (film_label, film_shift), (sub_label, sub_shift) in product(
                zip(film_terminations, film_shifts), zip(sub_terminations, sub_shifts)
            )
        }
        self.terminations = list(self._terminations)

    def get_interfaces(
        self,
        termination: tuple[str, str],
        gap: float = 2.0,
        vacuum_over_film: float = 20.0,
        film_thickness: float = 1,
        substrate_thickness: float = 1,
        in_layers: bool = True,
    ) -> Iterator[Interface]:
        film_sg = SlabGenerator(
            self.film_structure,
            self.film_miller,
            min_slab_size=film_thickness,
            min_vacuum_size=3,
            in_unit_planes=in_layers,
            center_slab=True,
            primitive=True,
            reorient_lattice=False,  # This is necessary to not screw up the lattice
        )

        sub_sg = SlabGenerator(
            self.substrate_structure,
            self.substrate_miller,
            min_slab_size=substrate_thickness,
            min_vacuum_size=3,
            in_unit_planes=in_layers,
            center_slab=True,
            primitive=True,
            reorient_lattice=False,  # This is necessary to not screw up the lattice
        )

        film_shift, sub_shift = self._terminations[termination]

        film_slab = film_sg.get_slab(shift=film_shift)
        sub_slab = sub_sg.get_slab(shift=sub_shift)
        
        film_slab = self.slab_film
        sub_slab = self.slab_substrate
        
        for match in self.zsl_matches:
            # Build film superlattice
            super_film_transform = np.round(
                from_2d_to_3d(get_2d_transform(film_slab.lattice.matrix[:2], match.film_sl_vectors))
            ).astype(int)
            film_sl_slab = film_slab.copy()
            film_sl_slab.make_supercell(super_film_transform)
            (
                assert_allclose(film_sl_slab.lattice.matrix[2], film_slab.lattice.matrix[2], atol=1e-08),
                "2D transformation affected C-axis for Film transformation",
            )
            (
                assert_allclose(film_sl_slab.lattice.matrix[:2], match.film_sl_vectors, atol=1e-08),
                "Transformation didn't make proper supercell for film",
            )
            film_sl_super_ouc = self.super_ouc_film.copy()
            film_sl_super_ouc.make_supercell(super_film_transform)
            (
                assert_allclose(film_sl_super_ouc.lattice.matrix[2], self.super_ouc_film.lattice.matrix[2], atol=1e-08),
                "2D transformation affected C-axis for Film transformation",
            )
            (
                assert_allclose(film_sl_super_ouc.lattice.matrix[:2], match.film_sl_vectors, atol=1e-08),
                "Transformation didn't make proper supercell for film",
            )
            
            # Build substrate superlattice
            super_sub_transform = np.round(
                from_2d_to_3d(get_2d_transform(sub_slab.lattice.matrix[:2], match.substrate_sl_vectors))
            ).astype(int)
            sub_sl_slab = sub_slab.copy()
            sub_sl_slab.make_supercell(super_sub_transform)
            (
                assert_allclose(sub_sl_slab.lattice.matrix[2], sub_slab.lattice.matrix[2], atol=1e-08),
                "2D transformation affected C-axis for Film transformation",
            )
            (
                assert_allclose(sub_sl_slab.lattice.matrix[:2], match.substrate_sl_vectors, atol=1e-08),
                "Transformation didn't make proper supercell for substrate",
            )
            sub_sl_super_ouc = self.super_ouc_substrate.copy()
            sub_sl_super_ouc.make_supercell(super_sub_transform)
            (
                assert_allclose(sub_sl_super_ouc.lattice.matrix[2], self.super_ouc_substrate.lattice.matrix[2], atol=1e-08),
                "2D transformation affected C-axis for Film transformation",
            )
            (
                assert_allclose(sub_sl_super_ouc.lattice.matrix[:2], match.substrate_sl_vectors, atol=1e-08),
                "Transformation didn't make proper supercell for substrate",
            )

            # Add extra info
            match_dict = match.as_dict()
            interface_properties = {k: match_dict[k] for k in match_dict if not k.startswith("@")}

            dfm = Deformation(match.match_transformation)

            strain = dfm.green_lagrange_strain
            interface_properties["strain"] = strain
            interface_properties["von_mises_strain"] = strain.von_mises_strain
            interface_properties["termination"] = termination
            interface_properties["film_thickness"] = film_thickness
            interface_properties["substrate_thickness"] = substrate_thickness

            yield Interface.from_slabs(
                substrate_slab=sub_sl_slab,
                film_slab=film_sl_slab,
                gap=gap,
                vacuum_over_film=vacuum_over_film,
                interface_properties=interface_properties,
            ), film_sl_super_ouc, sub_sl_super_ouc


class SurfaceGenerator:

    # NOTE: Please provide a conventional cell as bulk_structure, since: 
    # 1. Miller indices are defined based on the conventional cell.
    # 2. Conventional cells do not repeat in the a, b, and c directions.
    
    def __init__(self, bulk_structure, miller_index):
        self.bulk_structure = bulk_structure
        self.miller_index = miller_index
        
        self.composition_dict = get_composition_dict(self.bulk_structure.composition)
        
        self.surface = None
        self.num_layer = None
        self.symmetric = None
        self.stoichiometric = None
        self.slab_id = None
        
        self.original_slab = None
    
    def is_stoichiometric(self, structure, tol=1E-05):
        composition_dict = get_composition_dict(structure.composition)
        
        is_stoichiometric = True
        ratio = None
        for i in composition_dict:
            if i not in self.composition_dict:
                is_stoichiometric = False
                break
            
            if ratio == None:
                ratio = self.composition_dict[i] / composition_dict[i]
            else:
                if abs(self.composition_dict[i]/composition_dict[i]-ratio) > tol:
                    is_stoichiometric = False
                    break
        
        return is_stoichiometric
    
    @staticmethod
    def get_primitive_slab(slab, tol):
        original_ouc = slab.oriented_unit_cell.copy()
        original_miller_index = slab.miller_index
        original_shift = slab.shift
        original_scale_factor = slab.scale_factor
        original_reorient_lattice = slab.reorient_lattice
        
        ouc = slab.oriented_unit_cell.copy()
        
        slab = slab.get_primitive_structure(tolerance=tol)

        # Reorient the lattice to get the correct reduced cell
        # find a reduced ouc
        slab_l = slab.lattice
        ouc = ouc.get_primitive_structure(
            constrain_latt={
                "a": slab_l.a,
                "b": slab_l.b,
                "alpha": slab_l.alpha,
                "beta": slab_l.beta,
                "gamma": slab_l.gamma,
            }
        )
        # Check this is the correct oriented unit cell
        ouc = original_ouc if slab_l.a != ouc.lattice.a or slab_l.b != ouc.lattice.b else ouc
        
        # [POTENTIAL_BUG] After getting primitive cell, the scale factor should be modified, just like after LLL reducing! But here the original is retained!
        return PymatgenSlab(
            slab.lattice,
            slab.species_and_occu,
            slab.frac_coords,
            original_miller_index,
            ouc,
            original_shift,
            original_scale_factor, 
            energy=None,
            site_properties=slab.site_properties,
            reorient_lattice=original_reorient_lattice,
        )
    
    # NOTE: It is hard to include the mirrored asymmetric surface.
    # The user should create by themselves. The procedure is as follows:
    # If the surface is asymmetric, first make it orthogonal, 
    # and then multiply the third frac coord of each site by -1.
    
    def get_surface(
        self, 
        min_slab_thickness, 
        primitive=True, 
        symmetrize=False, 
        # include_mirrored_asymmetric_surface=True, 
        force_orthogonal=False, 
        spglib_tol=0.1, 
        fcluster_tol=0.1, 
        factor_slab_to_vacuum=3, 
    ):
        slab_generator = ModifiedSlabGenerator(
            initial_structure=self.bulk_structure, 
            miller_index=self.miller_index, 
            min_slab_size=2, 
            min_vacuum_size=2*factor_slab_to_vacuum, 
            lll_reduce=False, 
            center_slab=False, 
            in_unit_planes=True, 
            primitive=False, 
            max_normal_search=None, 
            reorient_lattice=True, 
        )
        
        slab, original_slab = slab_generator.get_slabs(
            bonds=None, 
            ftol=fcluster_tol, 
            tol=spglib_tol, 
            max_broken_bonds=0, 
            symmetrize=symmetrize, 
            repair=False, 
        )
        
        self.original_slab = original_slab
        
        num_slab = len(slab)
        
        self.surface = []
        self.num_layer = []
        self.symmetric = []
        self.stoichiometric = []
        self.slab_id = []
        for i in range(num_slab):
            num_layer = 1 if symmetrize else 0
            thickness = 0
            current_slab = None
            
            while thickness < min_slab_thickness:
                num_layer += 1
                
                slab_generator = ModifiedSlabGenerator(
                    initial_structure=self.bulk_structure, 
                    miller_index=self.miller_index, 
                    min_slab_size=num_layer, 
                    min_vacuum_size=num_layer*factor_slab_to_vacuum, 
                    lll_reduce=False, 
                    center_slab=False, 
                    in_unit_planes=True, 
                    primitive=False, 
                    max_normal_search=None, 
                    reorient_lattice=True, 
                )
                
                slab, original_slab = slab_generator.get_slabs(
                    bonds=None, 
                    ftol=fcluster_tol, 
                    tol=spglib_tol, 
                    max_broken_bonds=0, 
                    symmetrize=symmetrize, 
                    repair=False, 
                )
                
                assert len(slab) == num_slab, 'materials_science_utils.SurfaceGenerator.get_surface: len(slab) != num_slab, len(slab) = %s, num_slab = %s' % (len(slab), num_slab)
                
                if primitive:
                    current_slab = self.get_primitive_slab(slab[i], tol=spglib_tol)
                    current_slab.properties['slab_id'] = slab[i].properties['slab_id']
                else:
                    current_slab = slab[i]
                
                surface = Slab(Structure.from_sites(current_slab))
                surface.cluster_to_ref_atom(0)
                thickness = surface.calc_slab_thickness()
            
            self.surface.append(current_slab)
            self.num_layer.append(num_layer)
            self.symmetric.append(current_slab.is_symmetric())
            self.stoichiometric.append(self.is_stoichiometric(current_slab))
            self.slab_id.append(current_slab.properties['slab_id'])
            
            # if include_mirrored_asymmetric_surface and not(current_slab.is_symmetric()):
                # if symmetrize:
                    # assert current_slab.is_symmetric(), 'materials_science_utils.SurfaceGenerator.get_surface: symmetrize == True, but current_slab.is_symmetric() == False'
                
                # mirrored_slab = slab_generator.get_slab(shift=1-current_slab.shift)
                
                # self.surface.append(mirrored_slab)
                # self.num_layer.append(num_layer)
                # self.symmetric.append(mirrored_slab.is_symmetric())
                # self.stoichiometric.append(self.is_stoichiometric(mirrored_slab))
        
        if force_orthogonal:
            orthogonal_surface = [i.get_orthogonal_c_slab() for i in self.surface]
            
            for idx, i in enumerate(orthogonal_surface):
                i.properties['slab_id'] = self.surface[idx].properties['slab_id']
            
            self.surface = orthogonal_surface
    
    def get_orthogonal_surface_including_mirrored_asymmetric_surface(
        self, 
        min_slab_thickness, 
        primitive=True, 
        spglib_tol=0.1, 
        fcluster_tol=0.1, 
        factor_slab_to_vacuum=3, 
    ):
        self.get_surface(
            min_slab_thickness=min_slab_thickness, 
            primitive=primitive, 
            symmetrize=False, 
            force_orthogonal=True, 
            spglib_tol=spglib_tol, 
            fcluster_tol=fcluster_tol, 
            factor_slab_to_vacuum=factor_slab_to_vacuum, 
        )
        
        orthogonal_surface_including_mirrored_asymmetric_surface = []
        num_layer = []
        symmetric = []
        stoichiometric = []
        for idx, i in self.surface:
            if self.symmetric[idx]:
                orthogonal_surface_including_mirrored_asymmetric_surface.append(i)
                num_layer.append(self.num_layer[idx])
                symmetric.append(self.num_layer[idx])
                stoichiometric.append(self.num_layer[idx])
            else:
                orthogonal_surface_including_mirrored_asymmetric_surface.append(i)
                num_layer.append(self.num_layer[idx])
                symmetric.append(self.num_layer[idx])
                stoichiometric.append(self.num_layer[idx])
                
                structure = Structure.from_sites(i)


class ModifiedSlabGenerator(SlabGenerator):
    def get_slab(self, shift=0, tol: float = 0.1, energy=None):
        h = self._proj_height
        p = round(h / self.parent.lattice.d_hkl(self.miller_index), 8)
        if self.in_unit_planes:
            n_layers_slab = int(math.ceil(self.min_slab_size / p))
            n_layers_vac = int(math.ceil(self.min_vac_size / p))
        else:
            n_layers_slab = int(math.ceil(self.min_slab_size / h))
            n_layers_vac = int(math.ceil(self.min_vac_size / h))
        n_layers = n_layers_slab + n_layers_vac

        species = self.oriented_unit_cell.species_and_occu
        props = self.oriented_unit_cell.site_properties
        props = {k: v * n_layers_slab for k, v in props.items()}  # type: ignore[operator, misc]
        frac_coords = self.oriented_unit_cell.frac_coords
        frac_coords = np.array(frac_coords) + np.array([0, 0, -shift])[None, :]
        frac_coords -= np.floor(frac_coords)
        a, b, c = self.oriented_unit_cell.lattice.matrix
        new_lattice = [a, b, n_layers * c]
        frac_coords[:, 2] = frac_coords[:, 2] / n_layers
        all_coords = []
        for idx in range(n_layers_slab):
            f_coords = frac_coords.copy()
            f_coords[:, 2] += idx / n_layers
            all_coords.extend(f_coords)

        slab = Structure(new_lattice, species * n_layers_slab, all_coords, site_properties=props)

        scale_factor = self.slab_scale_factor
        # Whether or not to orthogonalize the structure
        if self.lll_reduce:
            lll_slab = slab.copy(sanitize=True)
            mapping = lll_slab.lattice.find_mapping(slab.lattice)
            assert mapping is not None, "LLL reduction has failed"  # mypy type narrowing
            scale_factor = np.dot(mapping[2], scale_factor)  # type: ignore[index]
            slab = lll_slab

        # Whether or not to center the slab layer around the vacuum
        if self.center_slab:
            avg_c = np.average([c[2] for c in slab.frac_coords])
            slab.translate_sites(list(range(len(slab))), [0, 0, 0.5 - avg_c])

        if self.primitive:
            prim = slab.get_primitive_structure(tolerance=tol)
            if energy is not None:
                energy = prim.volume / slab.volume * energy
            slab = prim

        # Reorient the lattice to get the correct reduced cell
        ouc = self.oriented_unit_cell.copy()
        if self.primitive:
            # find a reduced ouc
            slab_l = slab.lattice
            ouc = ouc.get_primitive_structure(
                constrain_latt={
                    "a": slab_l.a,
                    "b": slab_l.b,
                    "alpha": slab_l.alpha,
                    "beta": slab_l.beta,
                    "gamma": slab_l.gamma,
                }
            )
            # Check this is the correct oriented unit cell
            ouc = self.oriented_unit_cell if slab_l.a != ouc.lattice.a or slab_l.b != ouc.lattice.b else ouc

        # [ADDED] Put the thickness of slab (ouc version) into properties
        slab_thickness_super_ouc = abs(np.dot(self._normal, n_layers_slab*c))
        slab.properties['slab_thickness_super_ouc'] = slab_thickness_super_ouc

        slab_to_return =  PymatgenSlab(
            slab.lattice,
            slab.species_and_occu,
            slab.frac_coords,
            self.miller_index,
            ouc,
            shift,
            scale_factor,
            energy=energy,
            site_properties=slab.site_properties,
            reorient_lattice=self.reorient_lattice,
        )
        slab_to_return.properties=slab.properties
        
        return slab_to_return
    
    # NOTE: This method has been revised to enhance slab identification:
    # 1. The original implementation retained only one slab from each group of identical slabs,
    #    which complicated the tracking of slab origins.
    # 2. Previously, slabs lacked unique identifiers, further complicating the tracking process.
    # To address these issues, the overridden get_slabs() method now returns all original slabs in 
    # second position and assigns a unique ID to each slab, starting from 0, stored in 
    # slab.properties['slab_id'].

    def get_slabs(
        self,
        bonds=None,
        ftol=0.1,
        tol=0.1,
        max_broken_bonds=0,
        symmetrize=False,
        repair=False,
    ):
        c_ranges = [] if bonds is None else self._get_c_ranges(bonds)
        
        slabs = []
        for shift in self._calculate_possible_shifts(tol=ftol):
            bonds_broken = 0
            for r in c_ranges:
                if r[0] <= shift <= r[1]:
                    bonds_broken += 1
            slab = self.get_slab(shift, tol=tol, energy=bonds_broken)
            if bonds_broken <= max_broken_bonds:
                slabs.append(slab)
            elif repair:
                # If the number of broken bonds is exceeded,
                # we repair the broken bonds on the slab
                slabs.append(self.repair_broken_bonds(slab, bonds))
        
        for idx, i in enumerate(slabs):
            i.properties['slab_id'] = (idx, )
        
        original_slab = [i.copy(site_properties=i.site_properties) for i in slabs]
        for idx, i in enumerate(original_slab):
            i.properties = deepcopy(slabs[idx].properties)
            i.properties['slab_id'] = (idx, )
        
        # Further filters out any surfaces made that might be the same
        matcher = StructureMatcher(ltol=tol, stol=tol, primitive_cell=False, scale=False)
        
        new_slabs = []
        for g in matcher.group_structures(slabs):
            # For each unique termination, symmetrize the
            # surfaces by removing sites from the bottom.
            if symmetrize:
                slabs = self.nonstoichiometric_symmetrized_slab(g[0])
                
                for idx, i in enumerate(slabs):
                    i.properties['slab_id'] = (g[0].properties['slab_id'][0], idx)
                    i.properties['slab_thickness_super_ouc'] = g[0].properties['slab_thickness_super_ouc']
                
                new_slabs.extend(slabs)
            else:
                new_slabs.append(g[0])
        
        match = StructureMatcher(ltol=tol, stol=tol, primitive_cell=False, scale=False)
        new_slabs = [g[0] for g in match.group_structures(new_slabs)]
        
        return sorted(new_slabs, key=lambda s: s.energy), original_slab


class Slab:
    # MIND: If you want to set selective_dynamics, please use the method set_selective_dynamics 
    # instead of changing self.structure.site_properties directly.
    
    def __init__(self, structure):
        self.structure = structure.copy(properties=structure.properties, site_properties=structure.site_properties)
        
        self.selective_dynamics = False
        for i in self.structure:
            if 'selective_dynamics' in i.properties:
                self.selective_dynamics = True
                break
        
        if self.selective_dynamics:
            for i in self.structure:
                if 'selective_dynamics' not in i.properties:
                    i.properties['selective_dynamics'] = [True, True, True]
    
    def cluster_to_ref_atom(self, idx_ref_atom_0):
        self.structure = cluster_to_ref_atom(self.structure, idx_ref_atom_0)
    
    def calc_unit_ab_normal(self, unit_vector=True):
        ab_normal = np.cross(self.structure.lattice.matrix[0], self.structure.lattice.matrix[1])
        if unit_vector:
            unit_ab_normal = ab_normal / np.linalg.norm(ab_normal)
            
            return unit_ab_normal
        else:
            return ab_normal
    
    def calc_slab_thickness(self, direction='ab_normal'):
        '''
        direction: {'ab_normal', 'c'}
        '''
        length_along_c = calc_length(self.structure, direction=('c'))[0]
        
        if direction == 'ab_normal':
            unit_ab_normal = self.calc_unit_ab_normal()
            
            vector_c = self.structure.lattice.matrix[2]
            unit_vector_c = vector_c / self.structure.lattice.c
            
            return abs(np.dot(unit_ab_normal, unit_vector_c*length_along_c))
        elif direction == 'c':
            return length_along_c
        else:
            raise ValueError(
                "materials_science_utils.Slab.calc_slab_thickness: direction should be 'ab_normal' or 'c', however, direction == %s" % (direction)
            )
    
    def calc_slab_area(self):
        return abs(self.structure.lattice.a*self.structure.lattice.b*np.sin(np.deg2rad(self.structure.lattice.gamma)))
    
    def move_to_center(self):
        self.structure = move_to_center(self.structure, direction=('c'))
    
    def move_to_bottom(self):
        min_c = self.structure.frac_coords[:, 2].min()
        
        frac_coord = self.structure.frac_coords.copy()
        frac_coord[:, 2] -= min_c
        
        self.structure = Structure(
            lattice=self.structure.lattice, 
            species=self.structure.species, 
            coords=frac_coord, 
            site_properties=self.structure.site_properties, 
            properties=self.structure.properties, 
        )
    
    def reset_vacuum_thickness(self, thickness_vacuum, direction='ab_normal'):
        '''
        direction: {'ab_normal', 'c'}
        
        MIND: This method move your slab to the bottom of the lattice.
        '''
        vector_current_c = self.structure.lattice.matrix[2]
        length_current_c = self.structure.lattice.c
        unit_vector_current_c = vector_current_c / length_current_c
        
        thickness_along_c = self.calc_slab_thickness(direction='c')
        
        length_final_c = 0
        if direction == 'ab_normal':
            unit_ab_normal = self.calc_unit_ab_normal()
            
            cosine = abs(np.dot(unit_ab_normal, unit_vector_current_c))
            
            length_final_c = thickness_along_c + thickness_vacuum / cosine
        elif direction == 'c':
            length_final_c = thickness_along_c + thickness_vacuum
        else:
            raise ValueError(
                "materials_science_utils.Slab.set_vacuum_length: direction should be 'ab_normal' or 'c', however, direction == %s" % (direction)
            )
        
        scaling_factor = length_final_c / length_current_c
        
        final_lattice = self.structure.lattice.matrix.copy()
        final_lattice[2] *= scaling_factor
        
        self.move_to_bottom()
        
        frac_coord = self.structure.frac_coords.copy()
        frac_coord[:, 2] /= scaling_factor
        
        self.structure = Structure(
            lattice=final_lattice, 
            species=self.structure.species, 
            coords=frac_coord, 
            site_properties=self.structure.site_properties, 
            properties=self.structure.properties, 
        )
    
    def set_selective_dynamics(self, atom_idx_0, selective_dynamics=(False, False, False)):
        if self.selective_dynamics == False:
            self.selective_dynamics == True
            for i in self.structure:
                i.properties['selective_dynamics'] = (True, True, True)
        
        for i in atom_idx_0:
            self.structure[i].properties['selective_dynamics'] = selective_dynamics
    
    def set_selective_dynamics_within_thickness_range(
        self, 
        thickness_range=(0.00, 1.00), 
        selective_dynamics=(False, False, False), 
        tol=1E-05, 
    ):
        direction_idx = 2
        
        frac_range = []
        min_frac_coord = self.structure.frac_coords[:, direction_idx].min()
        max_frac_coord = self.structure.frac_coords[:, direction_idx].max()
        delta = max_frac_coord - min_frac_coord
        frac_range.append(min_frac_coord+delta*thickness_range[0]-tol)
        frac_range.append(min_frac_coord+delta*thickness_range[1]+tol)
        
        atom_idx_0 = []
        for idx, i in enumerate(self.structure):
            if frac_range[0] < i.frac_coords[direction_idx] < frac_range[1]:
                atom_idx_0.append(idx)
        
        self.set_selective_dynamics(atom_idx_0, selective_dynamics=selective_dynamics)
    
    def sort(self):
        self.structure.sort()
    
    def to_unit_cell(self):
        for i in self.structure:
            i.to_unit_cell(in_place=True)


class Molecule:
    def __init__(self, structure):
        self.structure = structure.copy(properties=structure.properties, site_properties=structure.site_properties)
    
    def cluster_to_ref_atom(self, idx_ref_atom_0):
        self.structure = cluster_to_ref_atom(self.structure, idx_ref_atom_0)
    
    def calc_center(self, cart=False):
        if cart:
            return np.mean(self.structure.cart_coords, axis=0)
        else:
            return np.mean(self.structure.frac_coords, axis=0)
    
    # TODO: I do not like this. Since we have the cluster_to_ref_atom method, 
    # the user should cluster first and then center. We should not put 
    # clustering into centring.
    def center(self, idx_ref_atom_0):
        self.cluster_to_ref_atom(idx_ref_atom_0)
        
        self.structure = Structure(
            self.structure.lattice, 
            self.structure.species, 
            self.structure.frac_coords+(0.5-self.calc_center()), 
        )
    
    # TODO: The same. We should not put centring into lattice changing. 
    # Let the user do this, otherwise the class is designed too complicated!
    def change_lattice(
        self, 
        new_lattice, 
        center={
            'on' : False, 
            'idx_ref_atom_0' : None, 
        }, 
    ):
        self.structure = Structure(
            new_lattice, 
            self.structure.species, 
            self.structure.cart_coords, 
            coords_are_cartesian=True, 
        )
        
        if center['on']:
            if not isinstance(center['idx_ref_atom_0'], int):
                raise ValueError(
                    "Molecule.change_lattice: not isinstance(center['idx_ref_atom_0'], int)"
                )
            
            self.center(center['idx_ref_atom_0'])
    
    def _calc_cart_coord(self, info_atom):
        lattice = self.structure.lattice
        
        if info_atom['method'] == 'direct':
            return lattice.get_cartesian_coords(self.structure[info_atom['idx_atom_0']].frac_coords)
        elif info_atom['method'] == 'center':
            center = np.zeros(3)
            for i in info_atom['idx_atom_0']:
                center += lattice.get_cartesian_coords(self.structure[i].frac_coords)
            center /= len(info_atom['idx_atom_0'])
            
            return center
    
    # TODO: This is good. For centring, we know clustering is necessary. 
    # For aligning, clustering is also necessary. Do you center or not? 
    # Overthinking is bad for class design!
    def align(self, info_atom_1, info_atom_2, target_direction='+c'):
        lattice = self.structure.lattice
        
        cart_coord_atom_1 = self._calc_cart_coord(info_atom_1)
        cart_coord_atom_2 = self._calc_cart_coord(info_atom_2)
        
        anchor = cart_coord_atom_1
        vector = cart_coord_atom_2 - cart_coord_atom_1
        
        if target_direction == '+a':
            target_direction = self.structure.lattice.matrix[0]
        elif target_direction == '-a':
            target_direction = -self.structure.lattice.matrix[0]
        elif target_direction == '+b':
            target_direction = self.structure.lattice.matrix[1]
        elif target_direction == '-b':
            target_direction = -self.structure.lattice.matrix[1]
        elif target_direction == '+c':
            target_direction = self.structure.lattice.matrix[2]
        elif target_direction == '-c':
            target_direction = -self.structure.lattice.matrix[2]
        else:
            pass
        
        axis = np.cross(vector, target_direction)
        theta = calc_angle_between_two_vector(vector, target_direction)
        
        self.structure.rotate_sites(
            indices=None, 
            theta=theta, 
            axis=axis, 
            anchor=anchor, 
            to_unit_cell=False, 
        )


def get_starting_index_of_element(structure, element):
    for i in range(len(structure)):
        if structure[i].specie.name == element:
            return i
    return 0
