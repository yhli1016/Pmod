from pmod.modmanager import ModManager
from .classes import *


# Module configurations
m = mod_manager = ModManager()

# System
m.create_mod('usrlocal', preset='lib', destination='/usr/local/lib')
m.create_mod('usrlocal', preset='lib', destination='/usr/local/lib64')

# For Intel_Parallel_Studio_XE 2018 update1
m.create_mod('IntelCC/2018.1.163', preset='void',
             environ=[('reset', 'FC', 'ifort'), ('reset', 'F90', 'ifort'),
                      ('reset', 'CC', 'icc'), ('reset', 'CXX', 'icpc')],
             command=['source /opt/intel/bin/compilervars.sh intel64'])

m.create_mod('MKL/2018.1.163', preset='void',
             command=['source /opt/intel/mkl/bin/mklvars.sh intel64'])

m.create_mod('IntelMPI/2018.1.163', mod_class=IntelMPI, preset='void',
             command=['source /opt/intel/impi/2018.1.163/bin64/mpivars.sh intel64'])

# OpenMPI
version = '1.6.5-gcc'
m.create_mod('openmpi/%s' % version, mod_class=OpenMPI165, preset='mod',
             destination='/opt/%s' % version)
version = '2.0.2-gcc'
m.create_mod('openmpi/%s' % version, mod_class=OpenMPI202, preset='mod',
             destination='/opt/%s' % version)
version = '3.1.3-intel'
m.create_mod('openmpi/%s' % version, mod_class=OpenMPI313, preset='mod',
             destination='/opt/%s' % version)

# Anaconda
m.create_mod('anaconda2/5.3.0', preset='mod', destination='/opt/anaconda2',
             conflict=['anaconda3/5.3.0'])
m.create_mod('anaconda3/5.3.0', preset='mod', destination='/opt/anaconda3',
             conflict=['anaconda2/5.3.0'])

# Phonopy
m.create_mod('phonopy/1.13.2', mod_class=IntelCCDer, preset='path',
             destination='/opt/phonopy/1.13.2/bin', depend=['anaconda2/5.3.0'],
             conflict=['anaconda3/5.3.0'])
m.create_mod('phonopy/1.13.2', preset='py',
             destination='/opt/phonopy/1.13.2/lib/python2.7/site-packages')

# ASE
m.create_mod('ASE/3.16.2', mod_class=IntelCCDer, preset='path',
             destination='/opt/ase/3.16.2/bin', depend=['anaconda2/5.3.0'],
             conflict=['anaconda3/5.3.0'])
m.create_mod('ASE/3.16.2', preset='py',
             destination='/opt/ase/3.16.2/lib/python2.7/site-packages')

# PYXAID
m.create_mod('PYXAID', mod_class=IntelMPIDer, preset='path',
             destination='/opt/PYXAID/bin', depend=['anaconda2/5.3.0'],
             conflict=['anaconda3/5.3.0'])
m.create_mod('PYXAID', preset='py', destination='/opt/PYXAID')

# GPAW
m.create_mod('gpaw/1.4.0', mod_class=IntelMPIDer, preset='path',
             destination='/opt/gpaw/1.4.0/bin',
             environ=[('reset', 'GPAW_SETUP_PATH',
                    '/opt/gpaw/1.4.0/data/gpaw-setups-0.9.20000')],
             depend=['anaconda2/5.3.0', 'ASE/3.16.2', 'MKL/2018.1.163',
                     'openblas/0.2.20'],
             conflict=['anaconda3/5.3.0'])
m.create_mod('gpaw/1.4.0', preset='py',
             destination='/opt/gpaw/1.4.0/lib/python2.7/site-packages')

# QE
m.create_mod('qe/6.3', mod_class=IntelMPIDer, preset='path',
             depend=['MKL/2018.1.163'], destination='/opt/qe/6.3/bin')

# VASP
for version in ['vasp/5.4.1', 'vasp/5.4.4']:
    m.create_mod(version, mod_class=IntelMPIDer, preset='path',
                 depend=['MKL/2018.1.163'], destination='/opt/%s/bin' % version)
m.create_mod('vtstscripts', preset='path',
             destination='/opt/vasp/vtstscripts-935')
m.create_mod('selfscripts', preset='path',
             destination='/opt/vasp/selfscripts')

# Gaussian
m.create_mod('Gaussian/09', preset='path', destination='/opt/g09',
             command=['source /opt/g09/bsd/g09.profile'],
             conflict=['Gaussian/16'])
m.create_mod('Gaussian/16', preset='path', destination='/opt/g16',
             command=['source /opt/g16/bsd/g16.profile'],
             conflict=['Gaussian/09'])

# CP2K
m.create_mod('cp2k/6.1.0', mod_class=IntelMPIDer, preset='path',
             depend=['MKL/2018.1.163'],
             destination='/opt/cp2k/6.1.0/exe/Linux-x86-64-intelx')

# ORCA
m.create_mod('orca/3.0.3', mod_class=OpenMPI165Der, preset='void',
             alias=[('orca3',
                  'nohup /opt/orca/3.0.3/bin/orca ../INCAR > ../OUTCAR &')])
m.create_mod('orca/4.0.1', mod_class=OpenMPI202Der, preset='void',
             alias=[('orca4',
                  'nohup /opt/orca/4.0.1/bin/orca ../INCAR > ../OUTCAR &')])
m.create_mod('orcascripts', preset='path', destination='/opt/orca/orcascripts')

# Shared libraries
libs = ['libint/1.1.6', 'libxc/4.0.4', 'libxsmm/1.9.0', 'libvdwxc/0.3.2',
        'fftw/3.3.8', 'elpa']
for lib in libs:
    m.create_mod(lib, mod_class=IntelCCDer, preset='mod',
                 destination='/opt/%s' % lib)

libs = ['blas/3.8.0', 'lapack/3.8.0', 'openblas/0.2.20']
for lib in libs:
    m.create_mod(lib, mod_class=IntelCCDer, preset='lib',
                 destination='/opt/%s' % lib)
