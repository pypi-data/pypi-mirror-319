"""
File Purpose: multifluid densities analysis from single-fluid muram data
"""

import numpy as np

from ...dimensions import SINGLE_FLUID
from ...defaults import DEFAULTS
from ...errors import (
    FluidValueError, FluidKeyError,
    InputError, FormulaMissingError, LoadingNotImplementedError,
)
from ...mhd import MhdMultifluidDensityLoader, Element, Specie
from ...tools import (
    simple_property,
    UNSET,
)


class MuramMultifluidDensityLoader(MhdMultifluidDensityLoader):
    '''density quantities based on Muram single-fluid values, & inferred multifluid properties.'''

    # # # N_MODE DISPATCH / CODE ARCHITECTURE # # #
    _VALID_N_MODES = ('best', 'elem', 'aux', 'saha', 'table', 'QN', 'QN_aux', 'QN_table')

    n_mode = simple_property('_n_mode', default='best', validate_from='_VALID_N_MODES',
        doc='''str. mode for getting Specie densities. (ignored if fluid is SINGLE_FLUID or an Element)
        Note that you can always calculate n using a specific formula with the appropriate var,
            regardless of n_mode. E.g. n_saha will always load value from saha.
        Options:
            'best' --> use best mode available, based on fluid:
                        electron --> 'aux' if eosne files exist, else 'table'
                        other Specie --> 'saha'
            'elem' --> n for fluid's Element, from abundances and SINGLE_FLUID r.
                        (crash if fluid.get_element() fails)
            'saha' --> from n_elem & saha ionization equation, assuming n=0 for twice+ ionized species.
                        (crash if not Specie)
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
                        (crash if not electron)
            'aux' --> load directly from file. 'eosne' for electrons. crash for other fluids.
                        (if not possible, crash or return NaN, depending on self.ntype_crash_if_nan)
            'QN', 'QN_aux', or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best', 'aux', or 'table' method.
                        (crash if not electron)
        Note: if ne_mode is not None, override n_mode with ne_mode when getting n for electrons.''')
    
    _VALID_NE_MODES = (None, 'best', 'aux', 'table', 'QN', 'QN_aux', 'QN_table')

    ne_mode = simple_property('_ne_mode', default=None, validate_from='_VALID_NE_MODES',
        doc='''None or str. mode for getting electron number density.
        None --> use n_mode for electrons instead of ne_mode.
        'best' --> 'aux' if simulation aux enabled, else 'table'.
        'aux' --> load value directly from eosne file if it exists,
                    else crash or NaN, depending on self.ntype_crash_if_nan.
        'table' --> infer from EOS table, using SINGLE_FLUID r and e.
        'QN', 'QN_aux', or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best', 'aux', or 'table' method.''')


    # # # GENERIC NUMBER DENSITY # # #

    @known_var(deps=[lambda ql, var, groups: ql._n_deps()])
    def get_n(self):
        '''number density. Formula depends on fluid:
        if SINGLE_FLUID, n = (r / m), where
            r is mass density directly from Bifrost snapshot, and
            m is abundance-weighted average particle mass; see help(self.get_m) for details.
        if Element, n = (r / m), where
            r is inferred from abundances combined with SINGLE_FLUID r, and
            m is element particle mass (fluid.m)
        if Specie, n depends on self.n_mode (and possibly self.ne_mode, if electron):
            'best' --> use best mode available, based on fluid:
                        electron --> 'aux' if eosne files exist, else 'table'
                        other Specie --> 'saha'
            'elem' --> n for fluid's Element, from abundances and SINGLE_FLUID r.
                        (crash if fluid.get_element() fails)
            'saha' --> from n_elem & saha ionization equation, assuming n=0 for twice+ ionized species,
                        using self('ne'), self('T'), fluid.saha_g1g0, and fluid.ionize_ev.
                        (crash if not Specie)
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
                        (crash if not electron)
            'aux' --> load directly from file. 'eosne' for electrons. crash for other fluids.
                        (if not possible, crash or return NaN, depending on self.ntype_crash_if_nan)
            'QN', 'QN_aux', or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best', 'aux', or 'table' methods.
                        (crash if not electron)
            if ne_mode not None, use ne_mode for electrons instead of n_mode.
        '''
        return super().get_n()  # see MhdMultifluidDensityLoader

    def _ntype(self, fluid=UNSET):
        '''return ntype for (single) fluid. See help(self.get_n) for details.
        if fluid is UNSET, use self.fluid. Must represent a single fluid.
        result depends on fluid as well as self.n_mode (and ne_mode if electron).

        Possible results (here, mode=ne_mode_explicit for electrons, n_mode for others):
            'SINGLE_FLUID': SINGLE_FLUID fluid
            'elem': Element.
                    Or, Specie when mode='elem' and fluid.element exists.
            'saha': non-electron Specie when mode='saha' or 'best'.
            'table': electron Specie when mode='table'.
                    Or, electron Specie when mode='best', and eosne aux file does not exist.
            'aux': electron Specie when mode='aux' (regardless of whether eosne aux file exists).
                    Or, electron Specie when mode='best' and eosne aux file exists.
            'QN_aux': electron Specie when mode='QN_aux'.
                    Or, electron Specie when mode='QN' and eosne file exists.
            'QN_table': electron Specie when mode='QN_table'.
                    Or, electron Specie when mode='QN' and eosne file does not exist.
            'nan': none of the above --> don't know how to get n for fluid.
        '''
        # [TODO][REF] call super(), instead of copying relevant logic from super()?
        #   however, it might be better to keep it as-is. Readability is important than efficiency here.
        using = dict() if fluid is UNSET else dict(fluid=fluid)
        with self.using(**using):
            f = self.fluid
            if self.fluid_is_iterable():
                raise FluidValueError(f'_ntype expects single fluid but got iterable: {f}')
            if f is SINGLE_FLUID:
                return 'SINGLE_FLUID'
            elif isinstance(f, Element):
                return 'elem'
            elif isinstance(f, Specie):
                # bookkeeping:
                aux_e = self._all_eos_aux_files_exist()
                electron = f.is_electron()
                mode = self.ne_mode_explicit if electron else self.n_mode
                # logic (same order as in docstring. readability is more important than efficiency here.)
                if mode == 'elem' and f.element is not None:
                    return 'elem'
                elif (not electron) and ((mode == 'saha') or (mode == 'best')):
                    return 'saha'
                elif electron:
                    if (mode == 'table') or ((mode == 'best') and (not aux_e)):
                        return 'table'
                    elif (mode == 'aux') or ((mode == 'best') and aux_e):
                        return 'aux'
                    elif (mode == 'QN_aux') or ((mode == 'QN') and aux_e):
                        return 'QN_aux'
                    elif (mode == 'QN_table') or ((mode == 'QN') and (not aux_e)):
                        return 'QN_table'
        return 'nan'

    def _get_n_dispatch(self, ntype, flist):
        '''return self('n') across all fluids in flist which share the same ntype.
        assumes self.fluid is already set to the fluids in flist.
        Subclass can override this method (instead of get_n) to add new ntypes.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        # super handles ntypes: SINGLE_FLUID, elem, saha, table, QN_table, and nan.
        if ntype == 'aux':
            return self('n_aux')
        elif ntype == 'QN_aux':
            return self('ne_QN', ne_mode='aux')
        else:
            return super()._get_n_dispatch(ntype, flist)

    def _n_deps_ntypes_dispatch(self, ntypes):
        '''return list of deps for n, based on ntypes.
        Subclass can override this method (instead of _n_deps) to add new ntypes.
        '''
        result = set(super()._n_deps_ntypes_dispatch(ntypes))
        # super() handles ntypes: SINGLE_FLUID, elem, saha, table, and QN_table.
        if 'aux' in ntypes:
            result.add('n_aux')
        if 'QN_aux' in ntypes:
            result.update(['ne_QN', 'n_aux'])
        return list(result)


    # # # NON-EQUILIBRIUM NUMBER DENSITY # # #

    @known_var(load_across_dims=['fluid'])
    def get_n_aux(self):
        '''number density of self.fluid specie(s); from aux files values.
        Result depends on fluid:
            electron --> 'eosne'
            other --> crash with FormulaMissingError.
        '''
        # load_across_dims for this one, instead of grouping via Partition & ntype,
        #   because here we don't expect multiple self.fluid with same formula,
        #   so there's basically no efficiency improvements from grouping.
        f = self.fluid
        if f.is_electron():
            return self('ne_aux')
        else:
            raise FormulaMissingError(f'n_aux for fluid {f}.')


    # # # NTYPE: SAHA # # #
    # inherited from MhdMultifluidDensityLoader


    # # # NTYPE: ELECTRON # # #

    @known_var  # [TODO] deps...
    def get_ne(self):
        '''electron number density.
        method based on self.ne_mode (use self.n_mode if ne_mode is None):
            'best' --> 'aux' if eosne files exist, else 'table'
            'aux' --> load value directly from eosne file if possible, else crash or NaN.
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
            'QN', 'QN_aux', or 'QN_table' --> sum of qi ni across self.fluids,
                    using 'best', 'aux', or 'table' methods when getting 'ne' for saha equation.
        '''
        # bookkeeping
        mode = self.ne_mode_explicit
        if mode == 'QN':
            mode = 'QN_aux' if self._all_eos_aux_files_exist() else 'QN_table'
        if mode == 'best':
            mode = 'aux' if self._all_eos_aux_files_exist() else 'table'
        # getting results:
        if mode == 'aux':
            result = self('ne_aux')
        elif mode == 'table':
            result = self('ne_fromtable')
        elif mode == 'QN_aux':
            result = self('ne_QN', ne_mode='aux')
        elif mode == 'QN_table':
            result = self('ne_QN', ne_mode='table')
        else:
            raise LoadingNotImplementedError(f'{type(self).__name__}.get_ne() when ne_mode={self.ne_mode_explicit!r}')
        return result

    # get_ne_QN() is inherited from MhdMultifluidDensityLoader.

    @known_var(dims=['snap'], ignores_dims=['fluid'])
    def get_ne_aux(self):
        '''electron number density, from 'hionne' in aux.
        hionne in aux is stored in cgs units.
        '''
        result = super().get_ne_aux()  # see MuramEosLoader
        return self._assign_electron_fluid_coord_if_unambiguous(result)
