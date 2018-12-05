from pmod.modmanager import ModManager

# Module configurations
m = mod_manager = ModManager()

# System
m.add_mod('usrlocal', preset='lib', destination='/usr/local/lib')
m.add_mod('usrlocal', preset='lib', destination='/usr/local/lib64')

# For Intel_Parallel_Studio_XE 2018 update1
m.add_mod('intel_2018_update1', preset='void',
          environ=[('reset', 'FC', 'ifort'), ('reset', 'F90', 'ifort'),
                   ('reset', 'CC', 'icc'), ('reset', 'CXX', 'icpc')])

# OpenMPI
m.add_mod('openmpi3_intel', preset='mod',
          destination='/opt/openmpi/3.1.3-intel',
          depend=['intel_2018_update1'],
          conflict=['openmpi2_gcc', 'openmpi1_gcc'])
m.add_mod('openmpi2_gcc', preset='mod',
          destination='/opt/openmpi/2.0.2-gcc',
          depend=['intel_2018_update1'],
          conflict=['openmpi3_intel', 'openmpi1_gcc'])
m.add_mod('openmpi1_gcc', preset='mod',
          destination='/opt/openmpi/1.6.5-gcc',
          depend=['intel_2018_update1'],
          conflict=['openmpi3_intel', 'openmpi2_gcc'])

# Anaconda
m.add_mod('anaconda2', preset='mod', destination='/opt/anaconda2',
          conflict=['anaconda3'])
m.add_mod('anaconda3', preset='mod', destination='/opt/anaconda3',
          conflict=['anaconda2'])

# Phonopy
m.add_mod('phonopy', preset='path', destination='/opt/phonopy/1.13.2/bin',
          depend=["anaconda2"])
m.add_mod('phonopy', preset='py',
          destination='/opt/phonopy/1.13.2/lib/python2.7/site-packages')

# ASE
m.add_mod('ASE', preset='path', destination='/opt/ase/3.16.2/bin',
          depend=["anaconda2"])
m.add_mod('ASE', preset='py',
          destination='/opt/ase/3.16.2/lib/python2.7/site-packages')

# PYXAID
m.add_mod('PYXAID', preset='path', destination='/opt/PYXAID/bin',
          depend=['anaconda2', 'intel_2018_update1'],
          conflict=['openmpi3_intel', 'openmpi2_gcc', 'openmpi1_gcc'])
m.add_mod('PYXAID', preset='py', destination='/opt/PYXAID')

# GPAW
m.add_mod('gpaw', preset='path', destination='/opt/gpaw/1.4.0/bin',
          environ=[('reset', 'GPAW_SETUP_PATH',
                    '/opt/gpaw/1.4.0/data/gpaw-setups-0.9.20000')],
          depend=['anaconda2', 'ASE', 'intel_2018_update1', 'openblas'],
          conflict=['openmpi3_intel', 'openmpi2_gcc', 'openmpi1_gcc'])
m.add_mod('gpaw', preset='py',
          destination='/opt/gpaw/1.4.0/lib/python2.7/site-packages')

# QE
m.add_mod('qe', preset='path', destination='/opt/qe/6.3/bin',
          depend=['intel_2018_update1'],
          conflict=['openmpi3_intel', 'openmpi2_gcc', 'openmpi1_gcc'])

# VASP
m.add_mod('vasp541', preset='path', destination='/opt/vasp/5.4.1/bin',
          depend=['intel_2018_update1'],
          conflict=['openmpi3_intel', 'openmpi2_gcc', 'openmpi1_gcc'])
m.add_mod('vasp544', preset='path', destination='/opt/vasp/5.4.4/bin',
          depend=['intel_2018_update1'],
          conflict=['openmpi3_intel', 'openmpi2_gcc', 'openmpi1_gcc'])
m.add_mod('vtstscripts', preset='path', destination='/opt/vasp/vtstscripts-935')
m.add_mod('selfscripts', preset='path', destination='/opt/vasp/selfscripts')

# Gaussian
m.add_mod('Gaussian09', preset='path', destination='/opt/g09')

# CP2K
m.add_mod('cp2k', preset='path',
          destination='/opt/cp2k/6.1.0/exe/Linux-x86-64-intelx',
          depend=['intel_2018_update1'],
          conflict=['openmpi3_intel', 'openmpi2_gcc', 'openmpi1_gcc'])

# ORCA
m.add_mod('orca3', preset='void', depend=['openmpi1_gcc'],
          conflict=['orca4', 'openmpi2_gcc'],
          command=["alias orca3='nohup /opt/orca/3.0.3/bin/orca ../INCAR > ../OUTCAR &'"])
m.add_mod('orca4', preset='void', depend=['openmpi2_gcc'],
          conflict=['orca3', 'openmpi1_gcc'],
          command=["alias orca4='nohup /opt/orca/4.0.1/bin/orca ../INCAR > ../OUTCAR &'"])
m.add_mod('orcascripts', preset='path', destination='/opt/orca/orcascripts')

# Shared libraries
m.add_mod('libint', preset='mod', destination='/opt/libint/1.1.6',
          depend=['intel_2018_update1'])
m.add_mod('libxc', preset='mod', destination='/opt/libxc/4.0.4',
          depend=['intel_2018_update1'])
m.add_mod('libxsmm', preset='mod', destination='/opt/libxsmm/1.9.0',
          depend=['intel_2018_update1'])
m.add_mod('libvdwxc', preset='mod', destination='/opt/libvdwxc/0.3.2',
          depend=['intel_2018_update1'])
m.add_mod('fftw3', preset='mod', destination='/opt/fftw/3.3.8',
          depend=['intel_2018_update1'])
m.add_mod('blas', preset='lib', destination='/opt/blas/3.8.0',
          depend=['intel_2018_update1'])
m.add_mod('lapack', preset='lib', destination='/opt/lapack/3.8.0',
          depend=['intel_2018_update1'])
m.add_mod('openblas', preset='lib', destination='/opt/openblas/0.2.20',
          depend=['intel_2018_update1'])
m.add_mod('elpa', preset='mod', destination='/opt/elpa',
          depend=['intel_2018_update1'])
