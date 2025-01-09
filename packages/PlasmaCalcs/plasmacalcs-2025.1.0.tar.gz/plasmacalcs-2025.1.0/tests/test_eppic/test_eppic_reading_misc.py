"""
File Purpose: misc tests for eppic hookup in PlasmaCalcs.
These tests require some simulation output.
Not intended to read lots of different values,
    just to read a few specific/misc. values to check if they work properly.
"""
import os
import pytest

# setting mp start method to fork (instead of 'spawn') prevents leaked semaphore objects. Not sure why.
# it also makes the tests a bit faster, maybe...
import multiprocessing as mp
mp.set_start_method('fork', force=True)

import numpy as np
import xarray as xr

import PlasmaCalcs as pc
pc.DEFAULTS.pic_ambiguous_unit = dict(u_t=1)  # must be defined before loading an EppicCalculator.

HERE = os.path.dirname(__file__)


''' --------------------- can create eppic calculator --------------------- '''

def get_eppic_calculator(**kw_init):
    '''make an eppic calculator'''
    with pc.InDir(os.path.join(HERE, 'test_eppic_tinybox')):
        ec = pc.EppicCalculator.from_here(**kw_init)
    return ec

def test_make_eppic_calculator():
    '''ensure can make an eppic calculator (with various inputs to __init__).'''
    get_eppic_calculator()
    get_eppic_calculator(snaps_from='timers')
    get_eppic_calculator(kw_units=dict(M=1))


''' --------------------- runtimes --------------------- '''

def test_reading_runtimes():
    '''test reading runtimes from eppic timers.dat'''
    ec = get_eppic_calculator()
    with pytest.raises(ValueError):
        ec('runtimes')  # fails because snap 0 file was deleted but timer is known for it.
    ec = get_eppic_calculator(snaps_from='timers')
    arr = ec('runtimes')  # just checking that this doesn't crash!
    arr = ec('calc_timestep_cost')
    assert arr.size == len(ec.snap)


''' --------------------- multi_slices --------------------- '''

def test_reading_multi_slices():
    '''test reading when using multi_slices.
    Also confirms Dataset.pc.size works properly.
    '''
    ec = get_eppic_calculator()
    with ec.using(multi_slices=dict(ndim=1, ikeep=0)):
        ds = ec('n')
    with ec.using(slices=dict(x=0)):
        arr_x0 = ec('n')
    with ec.using(slices=dict(y=0)):
        arr_y0 = ec('n')
    assert np.all(ds['keep_x'] == arr_y0)  # keep x <--> used y=0 slice
    assert np.all(ds['keep_y'] == arr_x0)  # keep y <--> used x=0 slice
    assert ds.pc.size == arr_x0.pc.size + arr_y0.pc.size


''' --------------------- enable_fromfile=False --------------------- '''

def test_enable_fromfile():
    '''test reading when using enable_fromfile=False.'''
    ec = get_eppic_calculator()
    # ensure can load normally
    m0 = ec('m', enable_fromfile=True)
    n0 = ec('n', enable_fromfile=True)
    # when load_direct_fromfile disabled, can load m (doesn't depend on file) but not n.
    m1 = ec('m', enable_fromfile=False)
    assert m1.identical(m0)
    with pytest.raises(pc.QuantCalcError):
        _should_crash = ec('n', enable_fromfile=False)
    # double-check that setting attribute via calculator produces the same behavior
    ec.enable_fromfile = True
    m2 = ec('m')
    assert m2.identical(m0)
    n2 = ec('n')
    assert n2.identical(n0)
    ec.enable_fromfile = False
    m3 = ec('m')
    assert m3.identical(m0)
    with pytest.raises(pc.QuantCalcError):
        _should_crash2 = ec('n')


''' --------------------- multiprocessing + parenthesis --------------------- '''

# takes roughly 7 seconds
def test_mp_with_parenthesis():
    '''ensure can run multiprocessing with parenthesis.'''
    # it can be tricky because parenthesis_memory is a class variable,
    # and pickling doesn't include changes to class or global variables, by default.
    # this ensures that the __getstate__ & __setstate__ solution works properly
    ec = get_eppic_calculator()
    ec.ncpu = 2
    ec('(n0)')
    ec('(deltafrac_n+1)*7')
    ec('mean_(n)')
    ec('nmean_(u**2)', stats_dimpoint_wise=False)
    ec('nmean_(u**2)', stats_dimpoint_wise=True)

# takes roughly 2 seconds, but run after test_mp_with_parenthesis,
#   so that we don't run this until we know ncpu>1 actually works on this machine.
def test_mp_timeout():
    '''ensure eppic calculator will timeout properly.'''
    # this test has print statements because pytest will print them if the test fails,
    #   and this test seems to fail inconsistently on some of the gitlab runners.
    #   the prints will hopefully help debug why it fails on some runners but not others.
    print(f'[test_mp_timeout] started', flush=True)  # flush=True --> print ASAP.
    ec = get_eppic_calculator()
    print(f'[test_mp_timeout] got eppic calculator', flush=True)
    NSNAP = 5000
    ec.snap = [i%10 for i in range(NSNAP)]  # a lot of snapshots (to make it take longer to read)
    longvar = 'stats_lowpass_(u_drift**2)'  # something that takes a while to calculate
    # check to ensure these calculations would take > 1s.
    print(f'[test_mp_timeout] about to check ec(longvar, ncpu=1) for 5 snaps', flush=True)
    with pc.Stopwatch(printing=False) as watch:  # check how long it takes to calculate for 5 snapshots.
        ec(longvar, ncpu=1, snap=ec.snap[:5])
    time5 = watch.time_elapsed()
    print(f'[test_mp_timeout] ec(longvar, ncpu=1) for 5 snaps took {time5:.2e} seconds', flush=True)
    assert time5 * NSNAP/5 > 1.1  # ensure longvar actually takes > 1s to calculate, when doing 5000 snaps.
    assert len(ec.snap) == 5000  # ensure original snaps restored
    # check timeout when ncpu=1 (i.e., single processing)
    with pc.Stopwatch(printing=False) as watch:
        print('[test_mp_timeout] starting ec(longvar, ncpu=1, timeout=1) for 5000 snaps', flush=True)
        with pytest.raises(pc.TimeoutError):
            ec(longvar, ncpu=1, timeout=1)   # ensure timeout works when ncpu=1
    print(f'[test_mp_timeout] ec(longvar, ncpu=1, timeout=1) for 5000 snaps took {watch.time_elapsed():.2e} seconds', flush=True)
    assert len(ec.snap) == 5000  # ensure original snaps restored even after TimeoutError.
    # check timeout when ncpu=2 (i.e., multiprocessing)
    with pc.Stopwatch(printing=False) as watch:
        print('[test_mp_timeout] starting ec(longvar, ncpu=2, timeout=1) for 5000 snaps', flush=True)
        with pytest.raises(pc.TimeoutError):
            ec(longvar, ncpu=2, timeout=1)   # ensure timeout works when ncpu>1
    print(f'[test_mp_timeout] ec(longvar, ncpu=2, timeout=1) for 5000 snaps took {watch.time_elapsed():.2e} seconds', flush=True)
