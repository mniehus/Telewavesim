from telewavesim import utils as ut
from telewavesim.rmat_f import plane as pw_f
from telewavesim import conf as cf
import numpy as np

def test_plane_obs():
    modfile='test_model_Audet2016.txt'
    cf.wvtype='P'
    ut.read_model(modfile)
    ut.model2for()

    cf.nt = 100
    cf.dt = 0.1
    cf.slow = 0.04
    cf.baz = 0.
    ut.wave2for()

    cf.dp = 1000.
    ut.obs2for()

    ux, uy, uz = pw_f.plane_obs(cf.nt, cf.nlay, np.array(cf.wvtype, dtype='c'))

    # seismogram should be maximized on vertical component
    assert np.max(np.abs(uz)) > np.max(np.abs(ux)) > np.max(np.abs(uy)), \
        'Energy is not maximized on vertical component'

    # tangential component should all be close to zero
    assert np.allclose(uy, np.zeros(len(uy))), 'non-zero values in uy'

def test_plane_land():
    modfile='test_model_Audet2016.txt'
    cf.wvtype='P'
    ut.read_model(modfile)
    ut.model2for()

    cf.nt = 2000
    cf.dt = 0.1
    cf.slow = 0.04
    cf.baz = 0.
    ut.wave2for()

    ut.check_cf()

    ux, uy, uz = pw_f.plane_land(cf.nt, cf.nlay, np.array(cf.wvtype, dtype='c'))

    # seismogram should be maximized on vertical component
    assert np.max(np.abs(uz)) > np.max(np.abs(ux)) > np.max(np.abs(uy)), \
        'Energy is not maximized on vertical component'

    # tangential component should all be close to zero
    assert np.allclose(uy, np.zeros(len(uy))), 'non-zero values in uy'

    trxyz = ut.get_trxyz(ux, uy, uz)
    tfs = ut.tf_from_xyz(trxyz)

    nt = tfs[0].stats.npts

    # zero-lag should be maximized on radial component
    assert tfs[0].data[int(nt/2)] > tfs[1].data[int(nt/2)], \
        'zero-lag is not maximized on radial component'
