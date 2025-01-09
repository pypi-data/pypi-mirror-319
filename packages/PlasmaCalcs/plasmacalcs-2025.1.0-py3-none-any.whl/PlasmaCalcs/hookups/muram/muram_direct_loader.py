"""
File Purpose: MuramDirectLoader
"""
import os

import numpy as np
import xarray as xr

from ...defaults import DEFAULTS
from ...dimensions import SnapHaver
from ...errors import CacheNotApplicableError, SnapValueError
from ...tools import (
    simple_property,
    product,
)


''' --------------------- MuramDirectLoader --------------------- '''

class MuramDirectLoader(SnapHaver):
    '''manages loading data directly from bifrost output files.'''

    # # # FILE PATH INFO # # #
    @property
    def snapdir(self):
        '''directory containing the snapshot files.
        Here, gives self.dirname, because Muram outputs are stored at top-level of directory.
        '''
        return self.dirname

    def snap_filepath(self, snap=None):
        '''convert snap to full file path for this snap, i.e. to the Header.NNN file.'''
        snap = self._as_single_snap(snap)
        return snap.filepath

    # # # DIRECT LOADING-RELATED INFO # # #
    def directly_loadable_vars(self, snap=None):
        '''return tuple of directly loadable variables for this snap.

        snap: None, str, int, Snap, or iterable indicating multiple snaps.
            the snapshot number to load. if None, use self.snap.
            if multiple snaps, return the result if all snaps have same result, else crash.
        '''
        kw = dict() if snap is None else dict(snap=snap)
        with self.using(**kw):
            multiple_snaps = self.snap_is_iterable()
            if multiple_snaps:
                snaps = self.snap
            else:
                snaps = [self._as_single_snap(snap)]
        result = None
        for snap in snaps:
            # result for this snap
            if hasattr(snap, 'exists_for') and not snap.exists_for(self):
                result_here = np.nan
            else:
                result_here = snap.directly_loadable_vars()
            # compare against known result
            if result is None:
                result = result_here
            elif result != result_here:
                errmsg = 'directly_loadable_vars differ between snaps. Retry with single snap instead.'
                raise SnapValueError(errmsg)
            # else, continue
        return result

    @property
    def data_array_shape(self):
        '''shape of each array of data stored in files. ('N0', 'N1', 'N2') from self.params.
        Shape with (x, y, z) dimensions is some transposition of the result;
        transpose order stored in 'layout.order' file, see also self.params['order'].
        '''
        return (self.params['N0'], self.params['N1'], self.params['N2'])

    @property
    def data_array_size(self):
        '''array size (number of elements) of each data array. (from data_array_shape)'''
        return product(self.data_array_shape)

    data_array_dtype = simple_property('_data_array_dtype', default=np.dtype('float32'),
            doc='''numpy dtype of each data array. default is np.dtype('float32').
            Used by np.memmap during self.load_fromfile.''')

    @property
    def data_array_nbytes(self):
        '''number of bytes in each data array. (from data_array_size and data_array_dtype)'''
        return self.data_array_size * self.data_array_dtype.itemsize

    data_array_order = simple_property('_data_array_order', default='F',
            doc='''ordering of data array axes: 'F' (Fortran) or 'C' (C order). Default 'F'.''')

    # # # LOAD DIRECT (add dimensions to var string) # # #
    _RESULT_PRIM_VAR_TO_FILEBASE = {
        'result_prim_r': 'result_prim_0',
        'result_prim_ux': 'result_prim_1',
        'result_prim_uy': 'result_prim_2',
        'result_prim_uz': 'result_prim_3',
        'result_prim_e': 'result_prim_4',
        'result_prim_bx': 'result_prim_5',
        'result_prim_by': 'result_prim_6',
        'result_prim_bz': 'result_prim_7',
    }

    def _var_dimmed(self, muram_var):
        '''return muram_var, possibly slightly adjusted based on currently-loading dimension(s).
        Here, follow the steps:
            (1) if self._loading_component, append self.component.
                E.g. 'result_prim_b' turns into 'result_prim_bz' when loading 'z' component.
            (2) convert result_prim_... via self._RESULT_PRIM_VAR_TO_FILEBASE, if applicable.
                E.g. 'result_prim_bx' becomes 'result_prim_5'.
        '''
        result = muram_var
        if getattr(self, '_loading_component', False):
            result = result + str(self.component)
        result = self._RESULT_PRIM_VAR_TO_FILEBASE.get(result, result)
        return result

    def load_direct(self, var, *args, **kw):
        '''load var "directly", either from a file, from cache or self.setvars, or from self.direct_overrides.
        Steps:
            1) attempt to get var from cache or self.setvars.
                [EFF] only tries this if we are not self._inside_quantity_loader_call_logic,
                to avoid redundant calls to self.get_set_or_cached.
            2) add dimensions to var if appropriate, based on the currently-loading dimension(s).
                See help(self._var_dimmed) for details.
            3) If added any dims, check if the dimmed var appears in self.setvars or self.cache.
            4) super().load_direct(dimmed_var, *args, **kw),
                which will use self.load_fromfile(...) unless any overrides apply here.

        note: does not check here if var (before adding dims) appears in self.setvars.
        '''
        # (0) - bookkeeping; delete any previous value of self._load_direct_used_override
        try:
            del self._load_direct_used_override
        except AttributeError:
            pass   # that's fine. Just want to reset it before running this function.
        # (1)
        if not getattr(self, '_inside_quantity_loader_call_logic', False):
            try:
                result = self.get_set_or_cached(var)
            except CacheNotApplicableError:
                pass
            else:
                self._load_direct_used_override = var
                return result
        # (2)
        muram_var = self._var_dimmed(var)
        # (3)
        if muram_var != var:  # check setvars & cache
            try:
                result = self.get_set_or_cached(muram_var)
            except CacheNotApplicableError:
                pass
            else:
                self._load_direct_used_override = muram_var
                return result
        # (4)
        return super().load_direct(muram_var, *args, **kw)

    # # # LOAD FROMFILE # # #
    def load_fromfile(self, muram_var, *args__None, snap=None, **kw__None):
        '''return numpy array of muram_var, loaded directly from file.

        muram_var: str
            the name of the variable to read. Should include all dimensions as appropriate.
            E.g. use 'bz' not 'b', to get magnetic field z-component.
        snap: None, str, int, or Snap
            the snapshot number to load. if None, use self.snap.
        '''
        snap = self._as_single_snap(snap)  # expect single snap when loading from file.
        if hasattr(snap, 'exists_for') and not snap.exists_for(self):
            result = xr.DataArray(self.snap_dim.NAN, attrs=dict(units='raw'))
            return self.assign_snap_coord(result)  # [TODO][EFF] assign coords when making array instead...
        filepath = os.path.join(snap.dirname, f'{muram_var}.{snap.s}')
        result = np.memmap(filepath,
                           mode='r',  # read-only; never alters existing files!
                           shape=self.data_array_shape,
                           dtype=self.data_array_dtype,
                           order=self.data_array_order,
                           )
        result = result.transpose(self.params['order'])  # transpose to match maindims order ('x', 'y', 'z').
        result = np.asarray(result)  # convert to numpy array.
        return result
