from pmod.modmanager import ModManager


# Module configurations
m = mod_manager = ModManager()

# System
m.add_mod('usrlocal', preset='lib', destination='/usr/local/lib')
m.add_mod('usrlocal', preset='lib', destination='/usr/local/lib64')

# For Intel_Parallel_Studio_XE 2018 update1
m.add_mod('IntelCC/2018.1.163', preset='void',
          environ=[('reset', 'FC', 'ifort'), ('reset', 'F90', 'ifort'),
                   ('reset', 'CC', 'icc'), ('reset', 'CXX', 'icpc')],
          command=['source /opt/intel/bin/compilervars.sh intel64',
                   'source /opt/intel/mkl/bin/mklvars.sh intel64'])
m.add_mod('IntelMPI/2018.1.163', preset='void',
          command=['source /opt/intel/impi/2018.1.163/bin64/mpivars.sh intel64'])

# OpenMPI
openmpi_versions = ['openmpi/%s' % version for version in
                    ['3.1.3-intel', '2.0.2-gcc', '1.6.5-gcc']]
for version in openmpi_versions:
    m.add_mod(version, preset='mod', destination='/opt/%s' % version,
              depend=['IntelCC/2018.1.163'],
              conflict=[ver2 for ver2 in openmpi_versions if ver2 != version])
    m.add_mod(version, preset='void', conflict=['IntelMPI/2018.1.163'])

# Anaconda
m.add_mod('anaconda2', preset='mod', destination='/opt/anaconda2',
          conflict=['anaconda3'])
m.add_mod('anaconda3', preset='mod', destination='/opt/anaconda3',
          conflict=['anaconda2'])

# Phonopy
m.add_mod('phonopy/1.13.2', preset='path',
          destination='/opt/phonopy/1.13.2/bin', depend=['anaconda2'])
m.add_mod('phonopy/1.13.2', preset='py',
          destination='/opt/phonopy/1.13.2/lib/python2.7/site-packages')

# ASE
m.add_mod('ASE/3.16.2', preset='path', destination='/opt/ase/3.16.2/bin',
          depend=['anaconda2'])
m.add_mod('ASE/3.16.2', preset='py',
          destination='/opt/ase/3.16.2/lib/python2.7/site-packages')

# PYXAID
m.add_mod('PYXAID', preset='path', destination='/opt/PYXAID/bin',
          depend=['anaconda2', 'IntelCC/2018.1.163', 'IntelMPI/2018.1.163'],
          conflict=openmpi_versions)
m.add_mod('PYXAID', preset='py', destination='/opt/PYXAID')

# GPAW
m.add_mod('gpaw/1.4.0', preset='path', destination='/opt/gpaw/1.4.0/bin',
          environ=[('reset', 'GPAW_SETUP_PATH',
                    '/opt/gpaw/1.4.0/data/gpaw-setups-0.9.20000')],
          depend=['anaconda2', 'ASE/3.16.2', 'IntelCC/2018.1.163',
                  'IntelMPI/2018.1.163', 'openblas/0.2.20'],
          conflict=openmpi_versions)
m.add_mod('gpaw/1.4.0', preset='py',
          destination='/opt/gpaw/1.4.0/lib/python2.7/site-packages')

# QE
m.add_mod('qe/6.3', preset='path', destination='/opt/qe/6.3/bin',
          depend=['IntelCC/2018.1.163', 'IntelMPI/2018.1.163'],
          conflict=openmpi_versions)

# VASP
for version in ['vasp/5.4.1', 'vasp/5.4.4']:
    m.add_mod(version, preset='path', destination='/opt/%s/bin'%version,
              depend=['IntelCC/2018.1.163', 'IntelMPI/2018.1.163'],
              conflict=openmpi_versions)
m.add_mod('vtstscripts', preset='path', destination='/opt/vasp/vtstscripts-935')
m.add_mod('selfscripts', preset='path', destination='/opt/vasp/selfscripts')

# Gaussian
m.add_mod('Gaussian09', preset='path', destination='/opt/g09',
          command=['source /opt/g09/bsd/g09.profile'], conflict=['Gaussian16'])
m.add_mod('Gaussian16', preset='path', destination='/opt/g16',
          command=['source /opt/g16/bsd/g16.profile'], conflict=['Gaussian09'])

# CP2K
m.add_mod('cp2k/6.1.0', preset='path',
          destination='/opt/cp2k/6.1.0/exe/Linux-x86-64-intelx',
          depend=['IntelCC/2018.1.163', 'IntelMPI/2018.1.163'],
          conflict=openmpi_versions)

# ORCA
m.add_mod('orca/3.0.3', preset='void',
          depend=['openmpi/1.6.5-gcc'],
          conflict=['openmpi/2.0.2-gcc', 'openmpi/3.1.3-intel',
                    'IntelMPI/2018.1.163'],
          alias=[('orca3',
                  'nohup /opt/orca/3.0.3/bin/orca ../INCAR > ../OUTCAR &')])
m.add_mod('orca/4.0.1', preset='void',
          depend=['openmpi/2.0.2-gcc'],
          conflict=['openmpi/1.6.5-gcc', 'openmpi/3.1.3-intel',
                    'IntelMPI/2018.1.163'],
          alias=[('orca4',
                  'nohup /opt/orca/4.0.1/bin/orca ../INCAR > ../OUTCAR &')])
m.add_mod('orcascripts', preset='path', destination='/opt/orca/orcascripts')

# Shared libraries
libs = ['libint/1.1.6', 'libxc/4.0.4', 'libxsmm/1.9.0', 'libvdwxc/0.3.2',
        'fftw/3.3.8', 'elpa']
for lib in libs:
    m.add_mod(lib, preset='mod', destination='/opt/%s'%lib,
              depend=['IntelCC/2018.1.163'])

libs = ['blas/3.8.0', 'lapack/3.8.0', 'openblas/0.2.20']
for lib in libs:
    m.add_mod(lib, preset='lib', destination='/opt/%s'%lib,
              depend=['IntelCC/2018.1.163'])