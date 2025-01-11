import os, logging, traceback
import h5py
import numpy as np
try:
    import imas
except:
    pass

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logger = logging.getLogger('imas_h5')
logger.addHandler(hnd)
logger.setLevel(logging.INFO)


def print_attrs(name, obj):
    # Create indent
    shift = name.count('/') * '    '
    item_name = name.split("/")[-1]
    print(shift + item_name)
    try:
        for key, val in obj.attrs.items():
            print(shift + '    ' + f"{key}: {val}")
    except:
        pass


class IMASids:

    def __init__(self, shot, run, tokamak='aug', version=os.getenv('IMAS_VERSION'), imasdb=os.getenv('IMASDB'), db='aug', backend='hdf5'):


        if 'imas' not in globals():
            logger.error('IMAS module not found, need module load imas?')
            return
        self.tokamak = tokamak
        self.db      = db
        self.version = version
        self.imasdb  = imasdb
        self.shot    = shot
        self.run     = run
        self.backend = backend
        
    def read_block(self, block):
        if self.backend == 'hdf5':
            self.ids = imas.DBEntry(imas.imasdef.HDF5_BACKEND, self.db, self.shot, self.run, user_name=self.imasdb)
        else:
            self.ids = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND, self.db, self.shot, self.run, user_name=self.imasdb)
        self.ids.open()
        setattr(self, block, self.ids.get(block))

    def read_array(self, block, branch, attr):
        if not hasattr(self, block):
            self.read_block(block)
        prof_obj = getattr(self.__dict__[block], branch)
        arr_out = np.array([])
        for val in prof_obj.array:
            arr_out = np.append(arr_out, val.__dict__[attr])
        return arr_out

        
def read_imas_h5(nshot, ids_run, imasdb=os.getenv('IMASDB'), db='aug', branch='core_profiles'):

    if os.getenv('IMASDB') is None:
        imasdb = '%s/public/imasdb' %os.getenv('HOME')

    h5_dir = '%s/%s/3/%d/%d' %(imasdb, db, nshot, ids_run)

# Core profiles

    fh5 = '%s/%s.h5' %(h5_dir, branch)

    try:
        logger.info('Reading %s' %fh5)
        f = h5py.File(fh5, 'r')
        return f
    except FileNotFoundError:
        traceback.print_exc()
        return None


if __name__ == '__main__':

    import matplotlib.pylab as plt

    fcp = read_imas_h5(36982, 7, branch='core_profiles')
    fsu = read_imas_h5(36982, 7, branch='summary')
    feq = read_imas_h5(36982, 7, branch='equilibrium')

    if fcp is not None:
        print(fcp.visititems(print_attrs))
        cp_t   = fcp['core_profiles/time'][:]
        cp_q   = fcp['core_profiles/profiles_1d[]&q'][:]
        cp_rho = fcp['core_profiles/profiles_1d[]&grid&rho_tor_norm'][:]
#        plt.plot(cp_rho[0], -cp_q[0])

    if fsu is not None:
        print(fsu.visititems(print_attrs))
        gq_t  = fsu['summary/time'][:]
        print(gq_t)
        gq_ip = fsu['summary/global_quantities&ip&value'][:]
        plt.plot(gq_t, gq_ip, label='summary')

    if feq is not None:
        print(feq.visititems(print_attrs))
        eq_t  = feq['equilibrium/time'][:]
        eq_ip = feq['equilibrium/time_slice[]&global_quantities&ip'][:]
        plt.plot(eq_t, eq_ip, label='equilibrium')
    plt.legend()
    plt.show()
