"""
File Purpose: densities for multifluid analysis of single-fluid mhd
"""
import numpy as np
import xarray as xr

from .mhd_multifluid_ionization import MhdMultifluidIonizationLoader
from .species import Specie
from ..elements import Element
from ..mhd_eos_loader import MhdEosLoader
from ...defaults import DEFAULTS
from ...dimensions import SINGLE_FLUID
from ...errors import (
    FluidValueError, FluidKeyError,
    InputError, FormulaMissingError, LoadingNotImplementedError,
)
from ...quantities import QuantityLoader
from ...tools import (
    alias, simple_property,
    UNSET,
    Partition,
    xarray_promote_dim,
)

class MhdMultifluidDensityLoader(MhdMultifluidIonizationLoader, MhdEosLoader):
    '''density quantities based on mhd single-fluid values, & inferred multifluid properties.'''

    # [TODO] (check is this actually correct?) inheritance notes:
    #   implementation here expects that EosLoader will be one of the parents.
    #   However, specifying it as a parent here directly will mess up the pattern of hookups
    #   which use, e.g. BifrostMultifluidCalculator(BifrostMultifluidStuff,
    #                           MhdMultifluidCalculator, BifrostCalculator),
    #   with BifrostCalculator inheriting from BifrostEosLoader which overrides some MhdEosLoader stuff.
    #   (if MhdMultifluidDensityLoader inherited from MhdEosLoader,
    #    then the BifrostMultifluidCalculator example above would use MhdEosLoader
    #    instead of BifrostEosLoader overrides.)


    # # # MISC DENSITY-RELATED VARS, OTHER THAN NUMBER DENSITY # # #

    @known_var(load_across_dims=['fluid'])
    def get_m(self):
        '''average mass of fluid particle.
        if SINGLE_FLUID, m computed as abundance-weighted average mass:
            m = self.elements.mtot() * (mass of 1 atomic mass unit).
            The "abundance-weighting" is as follows:
                m = sum_x(mx ax) / sum_x(ax), where ax = nx / nH, and x is any elem from self.elements.
                note: ax is related to abundance Ax via Ax = 12 + log10(ax).
            see help(self.elements.mtot) for more details, including a proof that mtot = rtot / ntot.
        if Element or Specie, return fluid.m, converted from [amu] to self.units unit system.
        '''
        f = self.fluid
        if f is SINGLE_FLUID:
            m_amu = super().get_m()
        else:
            m_amu = f.m * self.u('amu')
        return xr.DataArray(m_amu, attrs=self.units_meta())

    @known_var(load_across_dims=['fluid'])  # [TODO] deps
    def get_r(self):
        '''mass density.
        if SINGLE_FLUID, r directly from Bifrost;
        if Element, r inferred from SINGLE_FLUID r and abundances;
        if Species, r = n * m.
        '''
        # [TODO][EFF] improve efficiency by allowing to group species, e.g. via Partition();
        #    self('n') * self('m') will get a good speedup if grouped instead of load_across_dims.
        f = self.fluid
        if f is SINGLE_FLUID:
            return super().get_r()
        elif isinstance(f, Element):
            return self('r_elem')
        elif isinstance(f, Specie):
            return self('n') * self('m')
        raise LoadingNotImplementedError(f'{type(self).__name__}.get_r() for fluid of type {type(f)}')


    # # # N_MODE DISPATCH / CODE ARCHITECTURE # # #

    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['n_mode, ne_mode'], plus any behavior_attrs from super().
        '''
        return ['n_mode', 'ne_mode'] + list(getattr(super(), 'behavior_attrs', []))

    _VALID_N_MODES = ('best', 'elem', 'saha', 'table', 'QN', 'QN_table')

    n_mode = simple_property('_n_mode', default='best', validate_from='_VALID_N_MODES',
        doc='''str. mode for getting Specie densities. (ignored if fluid is SINGLE_FLUID or an Element)
        Note that you can always calculate n using a specific formula with the appropriate var,
            regardless of n_mode. E.g. n_saha will always load value from saha.
        Options:
            'best' --> use best mode available, based on fluid:
                        electron --> 'table'
                        Specie --> 'saha'
            'elem' --> n for fluid's Element, from abundances and SINGLE_FLUID r.
                        (crash if fluid.get_element() fails)
            'saha' --> from n_elem & saha ionization equation, assuming n=0 for twice+ ionized species.
                        (crash if not Specie)
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
                        (crash if not electron)
            'QN' or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best' or 'table' method.
                        (crash if not electron)
        Note: if ne_mode is not None, override n_mode with ne_mode when getting n for electrons.''')

    _VALID_NE_MODES = (None, 'best', 'table', 'QN', 'QN_table')
    
    ne_mode = simple_property('_ne_mode', default=None, validate_from='_VALID_NE_MODES',
        doc='''None or str. mode for getting electron number density.
        None --> use n_mode for electrons instead of ne_mode.
        'best' --> 'table'
        'table' --> infer from EOS table, using SINGLE_FLUID r and e.
        'QN' or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best' or 'table' method.''')

    ne_mode_explicit = alias('ne_mode', doc='''explicit ne_mode: ne_mode if not None, else n_mode.''')
    @ne_mode_explicit.getter
    def ne_mode_explicit(self):
        '''return ne_mode if set, else n_mode for electrons.'''
        ne_mode = self.ne_mode
        return self.n_mode if ne_mode is None else ne_mode

    # whether to crash during get_n methods if ntype 'nan'.
    # False --> return NaN for fluid(s) with ntype 'nan', instead of crashing.
    ntype_crash_if_nan = True

    def _get_n_nan(self):
        '''return n when ntype='nan' (or crash if ntype_crash_if_nan = True)'''
        if self.ntype_crash_if_nan:
            errmsg = (f'ntype "nan" for fluid(s): {self.fluid}.\n'
                      'To return NaN instead of crashing, set self.ntype_crash_if_nan=False.')
            raise FormulaMissingError(errmsg)
        # else:
        return xr.DataArray([np.nan for f in self.fluid], dims='fluid', coords={'fluid': self.fluid})

    # # # GENERIC NUMBER DENSITY # # #
    @known_var(deps=[lambda ql, var, groups: ql._n_deps()])
    def get_n(self):
        '''number density. Formula depends on fluid:
        if SINGLE_FLUID, n = (r / m), from SINGLE_FLUID r & m.
            default m is the abundance-weighted average particle mass; see help(self.get_m) for details.
        if Element, n = (r / m), where
            r is inferred from abundances combined with SINGLE_FLUID r, and
            m is element particle mass (fluid.m)
        if Specie, n depends on self.n_mode (and possibly self.ne_mode, if electron):
                'best' --> use best mode available, based on fluid:
                            electron --> 'table'
                            Specie --> 'saha'
                'elem' --> n for fluid's Element, from abundances and SINGLE_FLUID r.
                            (crash if fluid.get_element() fails)
                'saha' --> from n_elem & saha ionization equation, assuming n=0 for twice+ ionized species,
                            using self('ne'), self('T'), fluid.saha_g1g0, and fluid.ionize_ev.
                            (crash if not Specie)
                'table' --> infer from EOS table, using SINGLE_FLUID r and e.
                            (crash if not electron)
                'QN' or 'QN_table' --> sum of qi ni across self.fluids;
                            getting 'ne' for saha via 'best' or 'table' methods.
                            (crash if not electron)
            if ne_mode not None, use ne_mode for electrons instead of n_mode.
        '''
        squeeze_later = not self.fluid_is_iterable()
        part = Partition(self.fluid_list(), self._ntype)
        result = []
        for ntype, flist in part.items():
            with self.using(fluid=flist):
                result.append(self._get_n_dispatch(ntype, flist))
        result = self.join_fluids(result)
        if squeeze_later:  # single fluid only!
            result = xarray_promote_dim(result, 'fluid').squeeze('fluid')
        else:  # isel back to original order to match self.fluid order.
            result = result.isel(fluid=part.ridx_flat)
        return result

    @known_var(load_across_dims=['fluid'])
    def get_ntype(self):
        '''ntype for self.fluid; affects 'n' result, see help(self.get_n) for details.
        The output array will have dtype string.
        '''
        return xr.DataArray(self._ntype())

    def _n_deps(self=UNSET):
        '''returns the list of variables which are used to calculate n, based on self.fluid.'''
        if self is UNSET:
            errmsg = ('Cannot determine deps for var="n" when called as a classmethod. '
                       'n depends on the present value of self.fluid')
            raise InputError(errmsg)
        part = Partition(self.fluid_list(), self._ntype)
        return self._n_deps_ntypes_dispatch(part)


    # # # GENERIC NUMBER DENSITY -- DISPATCH; SUBCLASS CAN OVERRIDE TO ADD NEW NTYPES # # #
    # to add new ntypes, easiest if subclass overrides these methods, but not the methods above.
    # (maybe also override get_n to provide an updated docstring, but internally call super().get_n().)
    # see bifrost_number_densities.py for a good example of how to add new ntypes.

    def _ntype(self, fluid=UNSET):
        '''return ntype for (single) fluid. See help(self.get_n) for details.
        if fluid is UNSET, use self.fluid. Must represent a single fluid.
        result depends on fluid as well as self.n_mode (and ne_mode if electron).

        Possible results (here, mode=ne_mode_explicit for electrons, n_mode for others):
            'SINGLE_FLUID': SINGLE_FLUID fluid
            'elem': Element.
                    Or, Specie when mode='elem' and fluid.element exists.
            'saha': non-electron Specie when mode='saha'.
                    Or, non-electron Specie when mode='best'.
            'table': electron Specie when mode='table'.
                    Or, electron Specie when mode='best'.
            'QN_table': electron Specie when mode='QN' or 'QN_table'.
                    (note when mode='QN', get ne via 'best',
                    but 'best' will be 'table' in this class; subclass might override.)
            'nan': none of the above --> don't know how to get n for fluid.
        '''
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
                electron = f.is_electron()
                mode = self.ne_mode_explicit if electron else self.n_mode
                # logic (same order as in docstring. readability is more important than efficiency here.)
                if mode == 'elem' and f.element is not None:
                    return 'elem'
                elif mode == 'saha' and not electron:
                    return 'saha'
                elif mode == 'best' and not electron:
                    return 'saha'
                elif electron:
                    if mode == 'table':
                        return 'table'
                    elif mode == 'best':
                        return 'table'
                    elif mode == 'QN_table':
                        return 'QN_table'
                    elif mode == 'QN':
                        return 'QN_table'
        return 'nan'

    def _get_n_dispatch(self, ntype, flist):
        '''return self('n') across all fluids in flist which share the same ntype.
        assumes self.fluid is already set to the fluids in flist.
        Subclass can override this method (instead of get_n) to add new ntypes.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        if ntype == 'SINGLE_FLUID':
            if len(flist) > 1:
                raise NotImplementedError('[TODO] get_n with multiple SINGLE_FLUID...')
            with self.using(fluid=SINGLE_FLUID):
                return super().get_n().expand_dims('fluid')
        elif ntype == 'elem':
            return self('n_elem')
        elif ntype == 'saha':
            return self('n_saha')
        elif ntype == 'table':
            return self('ne_fromtable')
        elif ntype == 'QN_table':
            return self('ne_QN', ne_mode='table')
        elif ntype == 'nan':
            return self._get_n_nan()
        raise LoadingNotImplementedError(f'{type(self).__name__}.get_n() when ntype={ntype!r}')

    def _n_deps_ntypes_dispatch(self, ntypes):
        '''return list of deps for n, based on ntypes.
        Subclass can override this method (instead of _n_deps) to add new ntypes.
        '''
        result = set()
        if 'SINGLE_FLUID' in ntypes:
            result.update(['SF_r', 'SF_m'])
        if 'elem' in ntypes:
            result.add('n_elem')
        if 'saha' in ntypes:
            result.add('n_saha')
        if 'table' in ntypes:
            result.add('ne_fromtable')
        if 'QN_table' in ntypes:
            result.update(['ne_QN', 'ne_fromtable'])
        return list(result)


    # # # NTYPE: ELEM # # #

    @known_var(load_across_dims=['fluid'], aliases=['r_elem_per_rtot'])
    def get_rfrac_elem(self):
        '''mass density of element(s) for self.fluid, divided by total mass density.'''
        f = self.fluid
        if f is SINGLE_FLUID:
            return xr.DataArray(1)
        elif isinstance(f, (Element, Specie)):
            return xr.DataArray(f.get_element().r_per_nH() / self.elements.rtot_per_nH())
        else:
            raise NotImplementedError(f'fluid of type {type(f)} not yet supported for get_rfrac_elem')

    @known_var(load_across_dims=['fluid'], aliases=['n_elem_per_ntot'])
    def get_nfrac_elem(self):
        '''number density of element(s) for self.fluid, divided by total number density.'''
        f = self.fluid
        if f is SINGLE_FLUID:
            return xr.DataArray(1)
        elif isinstance(f, (Element, Specie)):
            return xr.DataArray(f.get_element().n_per_nH() / self.elements.ntot_per_nH())
        else:
            raise NotImplementedError(f'fluid of type {type(f)} not yet supported for get_nfrac_elem')

    @known_var(deps=['rfrac_elem', 'SF_r'])
    def get_r_elem(self):
        '''mass density of element(s) for self.fluid. r_elem = rfrac_elem * SF_r.'''
        return self('rfrac_elem') * self('SF_r')

    @known_var(deps=['nfrac_elem', 'SF_n'])
    def get_n_elem(self):
        '''number density of element(s) for self.fluid. n_elem = nfrac_elem * SF_n.'''
        return self('nfrac_elem') * self('SF_n')


    # # # NTYPE: SAHA # # #
    # (details of saha_n0 and saha_n1 are defined in MhdMultifluidIonizationLoader)

    @known_var(deps=[lambda ql, var, groups: ql._n_saha_deps()])
    def get_n_saha(self):
        '''number density of self.fluid specie(s), based on saha equation.
        neutral --> saha_n0, = n * (1 - ionfrac)
        once-ionized ion --> saha_n1, = n * ionfrac
        twice+ ionized ion --> 0
        SINGLE_FLUID, Element, or electron --> nan
        '''
        squeeze_later = not self.fluid_is_iterable()
        part = Partition(self.fluid_list(), self._ntype_saha)
        result = []
        for ntype, flist in part.items():
            with self.using(fluid=flist):
                if ntype == 'nan':
                    result.append(self._get_n_nan())
                elif ntype == '0':
                    arr_0 = xr.DataArray([0 for f in flist], dims='fluid', coords={'fluid': flist})
                    result.append(arr_0)
                elif ntype == 'saha_n0':  # [TODO][EFF] don't recalculate ionfrac terms for n0 and n1.
                    result.append(self('saha_n0'))
                elif ntype == 'saha_n1':
                    result.append(self('saha_n1'))
                else:
                    raise FormulaMissingError(f'ntype unknown: {ntype}')
        result = self.join_fluids(result)
        if squeeze_later:  # single fluid only!
            result = result.squeeze('fluid')
        else:  # isel back to original order to match self.fluid order.
            result = result.isel(fluid=part.ridx_flat)
        return result

    def _ntype_saha(self, fluid):
        '''return ntype for fluid with nfrom saha.
        SINGLE_FLUID --> 'nan'
        Element --> 'nan'
        Specie -->
            electron --> 'nan'
            neutral --> 'saha_n0'
            once-ionized ion --> 'saha_n1'
            twice+ ionized ion --> '0'
        '''
        if fluid is SINGLE_FLUID:
            return 'nan'
        elif isinstance(fluid, Element):
            return 'nan'
        elif isinstance(fluid, Specie):
            if fluid.is_electron():
                return 'nan'
            elif fluid.is_neutral():
                return 'saha_n0'
            elif fluid.q == 1:
                return 'saha_n1'
            elif fluid.q > 1:
                return '0'
        raise FormulaMissingError(f'saha_ntype for fluid {fluid}')

    def _n_saha_deps(self=UNSET):
        '''returns the list of variables which are used to calculate n_saha,
        based on self.fluid.
        '''
        if self is UNSET:
            errmsg = ('Cannot determine deps for var="n_saha" when called as a classmethod. '
                      'n_saha depends on the present value of self.fluid.')
            raise InputError(errmsg)
        part = Partition(self.fluid_list(), self._ntype_saha)
        result = set()
        if 'saha_n0' in part:
            result.add('saha_n0')
        if 'saha_n1' in part:
            result.add('saha_n1')
        return list(result)


    # # # NTYPE: ELECTRONS # # #
    @known_var  # [TODO] deps...
    def get_ne(self):
        '''electron number density.
        method based on self.ne_mode (use self.n_mode if ne_mode is None):
            'best' --> 'table'
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
            'QN' or 'QN_table' --> sum of qi ni across self.fluids;
                        getting 'ne' for saha via 'best' or 'table' method.
        '''
        # bookkeeping
        mode = self.ne_mode_explicit
        if mode == 'QN':
            mode = 'QN_table'
        if mode == 'best':
            mode = 'table'
        # getting results:
        if mode == 'table':
            result = self('ne_fromtable')
        elif mode == 'QN_table':
            result = self('ne_QN', ne_mode='table')
        else:
            raise LoadingNotImplementedError(f'{type(self).__name__}.get_ne() when ne_mode={self.ne_mode_explicit!r}')
        return result

    def _assign_electron_fluid_coord_if_unambiguous(self, array):
        '''return self.assign_fluid_coord(array, electron fluid).
        if self doesn't have exactly 1 electron fluid, don't assign coord.
        '''
        try:
            electron = self.fluids.get_electron()
        except FluidValueError:
            return array
        # else
        return self.assign_fluid_coord(array, electron, overwrite=True)

    @known_var(deps=['n', 'q'], ignores_dims=['fluid'])
    def get_ne_QN(self):
        '''electron number density, assuming quasineutrality.
        result is sum_i qi ni / |qe|, with sum across all ions i in self.fluids.
        (Comes from assuming sum_s qs ns = 0, with sum across all species s in self.fluids.)
        '''
        ions = self.fluids.ions()
        if 'QN' in self.ne_mode_explicit:
            errmsg = (f"cannot get 'ne_QN' when ne_mode (={self.ne_mode_explicit!r}) still implies QN; "
                      "need a non-QN way to get ne to use for saha equation.\n"
                      f"Valid ne_modes are: {self._VALID_NE_MODES}; consider using that doesn't imply QN.")
            raise FormulaMissingError(errmsg)
        ni = self('n', fluid=ions)  # <-- internally, ne for saha determined by self.ne_mode.
        Zi = self('q', fluid=ions) / self.u('qe')  # Zi = qi / |qe|
        result = Zi * ni
        result = xarray_promote_dim(result, 'fluid').sum('fluid')
        return self._assign_electron_fluid_coord_if_unambiguous(result)

    @known_var(deps=['SF_e', 'SF_r'], ignores_dims=['fluid'])
    def get_ne_fromtable(self):
        '''electron number density, from plugging r and e into eos tables (see self.tabin).'''
        result = super().get_ne_fromtable()  # see MhdEosLoader
        return self._assign_electron_fluid_coord_if_unambiguous(result)
