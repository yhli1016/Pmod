from pmod.modmanager import ModManager

# Module configurations
m = mod_manager = ModManager()

# Demonstration of managing multiple versions of modules
fftw_versions = ['fftw/%s' % ver for ver in ['3.3.4', '3.3.5', '3.3.6',
                 '3.3.7', '3.3.8']]
for ver1 in fftw_versions:
    m.add_mod(ver1, preset="mod", destination='/opt/%s' % ver1,
              conflict=[ver2 for ver2 in fftw_versions if ver2 != ver1])
