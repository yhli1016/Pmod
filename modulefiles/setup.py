from pmod.modmanager import ModManager


# Module configurations
m = mod_manager = ModManager()

# System
m.create_mod('usrlocal', preset='lib', destination='/usr/local/lib')
m.create_mod('usrlocal', preset='lib', destination='/usr/local/lib64')

# For Intel_Parallel_Studio_XE 2018 update1
m.create_mod('IntelCC/2018.1.163', preset='void',
             environ=[('reset', 'FC', 'ifort'), ('reset', 'F90', 'ifort'),
                   ('reset', 'CC', 'icc'), ('reset', 'CXX', 'icpc')],
             command=['source /opt/intel/bin/compilervars.sh intel64',
                   'source /opt/intel/mkl/bin/mklvars.sh intel64'])

# Intel MPI
openmpi_versions = ['openmpi/%s' % version for version in
                    ['3.1.3-intel', '2.0.2-gcc', '1.6.5-gcc']]
m.create_mod('IntelMPI/2018.1.163', preset='void', 
             depend=['IntelCC/2018.1.163'], conflict=openmpi_versions,
             command=['source /opt/intel/impi/2018.1.163/bin64/mpivars.sh intel64'])

# OpenMPI
for version in openmpi_versions:
    if version == 'openmpi/3.1.3-intel':
        m.create_mod(version, preset='mod', destination='/opt/%s' % version,
                     depend=['IntelCC/2018.1.163'],
                     conflict=[ver2 for ver2 in openmpi_versions 
                               if ver2 != version])
    else:
        m.create_mod(version, preset='mod', destination='/opt/%s' % version,
                     conflict=[ver2 for ver2 in openmpi_versions 
                               if ver2 != version])
    m.create_mod(version, preset='void', conflict=['IntelMPI/2018.1.163'])

# Anaconda
m.create_mod('anaconda2/5.3.0', preset='mod', destination='/opt/anaconda2',
             conflict=['anaconda3/5.3.0'])
m.create_mod('anaconda3/5.3.0', preset='mod', destination='/opt/anaconda3',
             conflict=['anaconda2/5.3.0'])

# Phonopy
m.create_mod('phonopy/1.13.2', preset='path',
             destination='/opt/phonopy/1.13.2/bin',
             depend=['IntelCC/2018.1.163', 'anaconda2/5.3.0'],
             conflict=['anaconda3/5.3.0'])
m.create_mod('phonopy/1.13.2', preset='py',
             destination='/opt/phonopy/1.13.2/lib/python2.7/site-packages')

# ASE
m.create_mod('ASE/3.16.2', preset='path', destination='/opt/ase/3.16.2/bin',
             depend=['IntelCC/2018.1.163', 'anaconda2/5.3.0'],
             conflict=['anaconda3/5.3.0'])
m.create_mod('ASE/3.16.2', preset='py',
             destination='/opt/ase/3.16.2/lib/python2.7/site-packages')

# PYXAID
m.create_mod('PYXAID', preset='path', destination='/opt/PYXAID/bin',
             depend=['anaconda2/5.3.0', 'IntelMPI/2018.1.163'],
             conflict=['anaconda3/5.3.0'])
m.create_mod('PYXAID', preset='py', destination='/opt/PYXAID')

# GPAW
m.create_mod('gpaw/1.4.0', preset='path', destination='/opt/gpaw/1.4.0/bin',
             environ=[('reset', 'GPAW_SETUP_PATH',
                       '/opt/gpaw/1.4.0/data/gpaw-setups-0.9.20000')],
             depend=['anaconda2/5.3.0', 'ASE/3.16.2',
                     'IntelMPI/2018.1.163', 'openblas/0.2.20'],
             conflict=['anaconda3/5.3.0'])
m.create_mod('gpaw/1.4.0', preset='py',
             destination='/opt/gpaw/1.4.0/lib/python2.7/site-packages')

# QE
m.create_mod('qe/6.3', preset='path', destination='/opt/qe/6.3/bin',
             depend=['IntelMPI/2018.1.163'])

# VASP
for version in ['vasp/5.4.1', 'vasp/5.4.4']:
    m.create_mod(version, preset='path', destination='/opt/%s/bin' % version,
                 depend=['IntelMPI/2018.1.163'])
m.create_mod('vtstscripts', preset='path', destination='/opt/vasp/vtstscripts-935')
m.create_mod('selfscripts', preset='path', destination='/opt/vasp/selfscripts')

# Gaussian
m.create_mod('Gaussian/09', preset='path', destination='/opt/g09',
             command=['source /opt/g09/bsd/g09.profile'],
             conflict=['Gaussian/16'])
m.create_mod('Gaussian/16', preset='path', destination='/opt/g16',
             command=['source /opt/g16/bsd/g16.profile'],
             conflict=['Gaussian/09'])

# CP2K
m.create_mod('cp2k/6.1.0', preset='path',
             destination='/opt/cp2k/6.1.0/exe/Linux-x86-64-intelx',
             depend=['IntelMPI/2018.1.163'])

# ORCA
m.create_mod('orca/3.0.3', preset='void',
             depend=['openmpi/1.6.5-gcc'],
             alias=[('orca3',
                  'nohup /opt/orca/3.0.3/bin/orca ../INCAR > ../OUTCAR &')])
m.create_mod('orca/4.0.1', preset='void',
             depend=['openmpi/2.0.2-gcc'],
             alias=[('orca4',
                  'nohup /opt/orca/4.0.1/bin/orca ../INCAR > ../OUTCAR &')])
m.create_mod('orcascripts', preset='path', destination='/opt/orca/orcascripts')

# Shared libraries
libs = ['libint/1.1.6', 'libxc/4.0.4', 'libxsmm/1.9.0', 'libvdwxc/0.3.2',
        'fftw/3.3.8', 'elpa']
for lib in libs:
    m.create_mod(lib, preset='mod', destination='/opt/%s' % lib,
                 depend=['IntelCC/2018.1.163'])

libs = ['blas/3.8.0', 'lapack/3.8.0', 'openblas/0.2.20']
for lib in libs:
    m.create_mod(lib, preset='lib', destination='/opt/%s' % lib,
                 depend=['IntelCC/2018.1.163'])
