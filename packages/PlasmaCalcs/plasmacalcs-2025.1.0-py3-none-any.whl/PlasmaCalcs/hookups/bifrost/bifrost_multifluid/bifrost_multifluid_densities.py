"""
File Purpose: loading Bifrost number densities
"""
import numpy as np

from ....dimensions import SINGLE_FLUID
from ....defaults import DEFAULTS
from ....errors import (
    FluidValueError, FluidKeyError,
    InputError, FormulaMissingError, LoadingNotImplementedError,
)
from ....mhd import MhdMultifluidDensityLoader, Element, Specie
from ....tools import (
    simple_property,
    UNSET,
)

class BifrostMultifluidDensityLoader(MhdMultifluidDensityLoader):
    '''density quantities based on Bifrost single-fluid values, & inferred multifluid properties.'''

    # # # N_MODE DISPATCH / CODE ARCHITECTURE # # #
    _VALID_N_MODES = ('best', 'elem', 'neq', 'saha', 'table', 'QN', 'QN_neq', 'QN_table')

    n_mode = simple_property('_n_mode', default='best', validate_from='_VALID_N_MODES',
        doc='''str. mode for getting Specie densities. (ignored if fluid is SINGLE_FLUID or an Element)
        Note that you can always calculate n using a specific formula with the appropriate var,
            regardless of n_mode. E.g. n_neq will always load non-equilirbium value.
        Options:
            'best' --> use best mode available, based on fluid:
                        electron --> 'neq' if simulation neq enabled, else 'table'.
                        H or He Specie --> 'neq' if simulation neq enabled, else 'saha'
                        other Specie --> 'saha'
            'elem' --> n for fluid's Element, from abundances and SINGLE_FLUID r.
                        (crash if fluid.get_element() fails)
            'neq' --> load value directly from file if simulation neq enabled.
                        (if not possible, crash or return NaN, depending on self.ntype_crash_if_nan)
            'saha' --> from n_elem & saha ionization equation, assuming n=0 for twice+ ionized species.
                        (crash if not Specie)
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
                        (crash if not electron)
            'QN', 'QN_neq', or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best', 'neq', or 'table' method.
                        (crash if not electron)
        Note: if ne_mode is not None, override n_mode with ne_mode when getting n for electrons.''')
    
    _VALID_NE_MODES = (None, 'best', 'neq', 'table', 'QN', 'QN_neq', 'QN_table')

    ne_mode = simple_property('_ne_mode', default=None, validate_from='_VALID_NE_MODES',
        doc='''None or str. mode for getting electron number density.
        None --> use n_mode for electrons instead of ne_mode.
        'best' --> 'neq' if simulation neq enabled, else 'table'.
        'neq' --> load value directly from file if simulation neq enabled,
                    else crash or NaN, depending on self.ntype_crash_if_nan.
        'table' --> infer from EOS table, using SINGLE_FLUID r and e.
        'QN', 'QN_neq', or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best', 'neq', or 'table' method.''')


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
                        electron --> 'neq' if simulation neq enabled, else 'table'.
                        H or He Specie --> 'neq' if simulation neq enabled, else 'saha'
                        other Specie --> 'saha'
            'elem' --> n for fluid's Element, from abundances and SINGLE_FLUID r.
                        (crash if fluid.get_element() fails)
            'neq' --> load value directly from file if simulation neq enabled.
                        neq possibly available in aux:
                            e-     --> 'hionne'
                            H_I    --> sum('n1', 'n2', 'n3', 'n4', 'n5')
                            H_II   --> 'n6'
                            He_I   --> 'nhe1'  (actually, exp('nhe1'); aux stores log values)
                            He_II  --> 'nhe2'  (actually, exp('nhe2'); aux stores log values)
                            He_III --> 'nhe3'  (actually, exp('nhe3'); aux stores log values)
                        (if not possible, crash or return NaN, depending on self.ntype_crash_if_nan)
            'saha' --> from n_elem & saha ionization equation, assuming n=0 for twice+ ionized species,
                        using self('ne'), self('T'), fluid.saha_g1g0, and fluid.ionize_ev.
                        (crash if not Specie)
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
                        (crash if not electron)
            'QN', 'QN_neq', or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best', 'neq', or 'table' methods.
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
            'neq': e or H Specie when mode='neq' (regardless of whether simulation neq enabled).
                    Or, e, H, or He Specie when mode='best' or 'neq' and simulation neq enabled.
                    (simulation neq enabled for e and H if params['do_hion']. also for He if 'do_helium')
            'saha': non-electron Specie when mode='saha'.
                    Or, non-electron Specie when mode='best', and simulation neq disabled.
            'table': electron Specie when mode='table'.
                    Or, electron Specie when mode='best', and simulation neq mode disabled.
            'QN_neq': electron Specie when mode='QN_neq'.
                    Or, electron Specie when mode='QN' and simulation neq enabled.
            'QN_table': electron Specie when mode='QN_table'.
                    Or, electron Specie when mode='QN' and simulation neq disabled.
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
                neq_H = self.params.get('do_hion', False)
                neq_e = neq_H  # if neq_H, also have neq_e.
                neq_He = self.params.get('do_helium', False)
                electron = f.is_electron()
                H = f.element == 'H'
                He = f.element == 'He'
                if electron or H:
                    neq_enabled = self.params.get('do_hion', False)
                elif He:
                    neq_enabled = self.params.get('do_helium', False)
                else:
                    neq_enabled = False
                mode = self.ne_mode_explicit if electron else self.n_mode
                # logic (same order as in docstring. readability is more important than efficiency here.)
                if mode == 'elem' and f.element is not None:
                    return 'elem'
                elif mode == 'neq' and (electron or H):
                    return 'neq'
                elif (mode == 'best' or mode == 'neq') and neq_enabled:
                    return 'neq'
                elif mode == 'saha' and not electron:
                    return 'saha'
                elif mode == 'best' and not electron and not neq_enabled:
                    return 'saha'
                elif electron:
                    if mode == 'table':
                        return 'table'
                    elif mode == 'best' and not neq_enabled:
                        return 'table'
                    elif mode == 'QN_neq':
                        return 'QN_neq'
                    elif mode == 'QN' and neq_enabled:
                        return 'QN_neq'
                    elif mode == 'QN_table':
                        return 'QN_table'
                    elif mode == 'QN' and not neq_enabled:
                        return 'QN_table'
        return 'nan'

    def _get_n_dispatch(self, ntype, flist):
        '''return self('n') across all fluids in flist which share the same ntype.
        assumes self.fluid is already set to the fluids in flist.
        Subclass can override this method (instead of get_n) to add new ntypes.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        # super handles ntypes: SINGLE_FLUID, elem, saha, table, QN_table, and nan.
        if ntype == 'neq':
            return self('n_neq')
        elif ntype == 'QN_neq':
            return self('ne_QN', ne_mode='neq')
        else:
            return super()._get_n_dispatch(ntype, flist)

    def _n_deps_ntypes_dispatch(self, ntypes):
        '''return list of deps for n, based on ntypes.
        Subclass can override this method (instead of _n_deps) to add new ntypes.
        '''
        result = set(super()._n_deps_ntypes_dispatch(ntypes))
        # super() handles ntypes: SINGLE_FLUID, elem, saha, table, and QN_table.
        if 'neq' in ntypes:
            result.add('n_neq')
        if 'QN_neq' in ntypes:
            result.update(['ne_QN', 'n_neq'])
        return list(result)


    # # # NON-EQUILIBRIUM NUMBER DENSITY # # #

    @known_var(load_across_dims=['fluid'])
    def get_n_neq(self):
        '''number density of self.fluid specie(s); non-equilibrium values.
        Result depends on fluid:
            electron --> 'hionne'
            'H_I'    --> sum('n1', 'n2', 'n3', 'n4', 'n5')
            'H_II'   --> 'n6'
            'He_I'   --> 'nhe1'  (actually, exp('nhe1'); aux stores log values)
            'He_II'  --> 'nhe2'  (actually, exp('nhe2'); aux stores log values)
            'He_III' --> 'nhe3'  (actually, exp('nhe3'); aux stores log values)
            other --> crash with FormulaMissingError.
        the electron fluid is tested via fluid.is_electron(),
        while the other species are tested via name-matching to the names above.
        '''
        # load_across_dims for this one, instead of grouping via Partition & ntype,
        #   because here we don't expect multiple self.fluid with same formula,
        #   so there's basically no efficiency improvements from grouping.
        f = self.fluid
        if f.is_electron():
            return self('ne_neq')
        elif f == 'H_I':
            n1 = self('load_n1')
            n2 = self('load_n2')
            n3 = self('load_n3')
            n4 = self('load_n4')
            n5 = self('load_n5')
            result_cgs = n1 + n2 + n3 + n4 + n5
        elif f == 'H_II':
            result_cgs = self('load_n6')
        elif f == 'He_I':
            result_cgs = np.exp(self('load_nhe1'))
        elif f == 'He_II':
            result_cgs = np.exp(self('load_nhe2'))
        elif f == 'He_III':
            result_cgs = np.exp(self('load_nhe3'))
        else:
            raise FormulaMissingError(f'n_neq for fluid {f}.')
        result_cgs = self._upcast_if_max_n_requires_float64(result_cgs)  # <- maybe make float64.
        result = result_cgs * self.u('n', convert_from='cgs')  # <- convert to self.units system.
        return self.record_units(result)


    # # # NTYPE: SAHA # # #
    # inherited from MhdMultifluidDensityLoader


    # # # NTYPE: ELECTRON # # #

    @known_var  # [TODO] deps...
    def get_ne(self):
        '''electron number density.
        method based on self.ne_mode (use self.n_mode if ne_mode is None):
            'best' --> 'neq' if simulation neq enabled, else 'table'
            'neq' --> load value directly from file if simulation neq enabled, else crash or NaN.
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
            'QN', 'QN_neq', or 'QN_table' --> sum of qi ni across self.fluids,
                    using 'best', 'neq', or 'table' methods when getting 'ne' for saha equation.
        '''
        # bookkeeping
        mode = self.ne_mode_explicit
        if mode == 'QN':
            mode = 'QN_neq' if self.params.get('do_hion', False) else 'QN_table'
        if mode == 'best':
            mode = 'neq' if self.params.get('do_hion', False) else 'table'
        # getting results:
        if mode == 'neq':
            result = self('ne_neq')
        elif mode == 'table':
            result = self('ne_fromtable')
        elif mode == 'QN_neq':
            result = self('ne_QN', ne_mode='neq')
        elif mode == 'QN_table':
            result = self('ne_QN', ne_mode='table')
        else:
            raise LoadingNotImplementedError(f'{type(self).__name__}.get_ne() when ne_mode={self.ne_mode_explicit!r}')
        return result

    # get_ne_QN() is inherited from MhdMultifluidDensityLoader.

    @known_var(dims=['snap'], ignores_dims=['fluid'])
    def get_ne_neq(self):
        '''electron number density, from 'hionne' in aux.
        hionne in aux is stored in cgs units.
        '''
        result = super().get_ne_neq()  # see BifrostEosLoader
        return self._assign_electron_fluid_coord_if_unambiguous(result)

