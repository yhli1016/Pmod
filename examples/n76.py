from pmod.modmanager import ModManager


# Module configurations
m = mod_manager = ModManager()
prefix = "/home/yhli/soft/"

# for shared libraries
m.add_mod("mkl/13.0.079", preset="path",
          destination=prefix+"mkl-13.0.079/bin")
m.add_mod("mkl/13.0.079", preset="inc",
          destination=prefix+"mkl-13.0.079/include")
m.add_mod("mkl/13.0.079", preset="lib",
          destination=prefix+"mkl-13.0.079/lib/intel64")
m.add_mod("fftw/3.3.4", preset="mod", destination=prefix+"fftw-3.3.4")
m.add_mod("hdf5/1.8.17", preset="mod", destination=prefix+"hdf5-1.8.17")
m.add_mod("libxc/4.2.3", preset="mod", destination=prefix+"libxc-4.2.3")

# for openmpi
m.add_mod("openmpi/1.10.0", preset="mod", destination=prefix+"openmpi-1.10.0")

# for DFT and GW software
m.add_mod("qe/6.2", preset="path", destination=prefix+"qe-6.2/bin",
          depend=["mkl/13.0.079", "openmpi/1.10.0", "hdf5/1.8.17"],
          conflict=["qe/5.4.0"])

m.add_mod("qe/5.4.0", preset="path",
          destination=prefix +"espresso-5.4.0/bin",
          depend=["mkl/13.0.079", "openmpi/1.10.0"],
          conflict=["qe/6.2"])

m.add_mod("bgw/1.2.0", preset="path", destination=prefix+"bgw-1.2.0/bin",
          depend=["mkl/13.0.079", "openmpi/1.10.0", "hdf5/1.8.17",
                  "fftw/3.3.4"])

m.add_mod("elk/4.0.15", preset="path", destination=prefix+"elk/4.0.15/bin",
          depend=["mkl/13.0.079", "openmpi/1.10.0"])

m.add_mod("wannier90/2.1.0", preset="path",
          destination=prefix+"wannier90-2.1.0",
          depend=["mkl/13.0.079", "openmpi/1.10.0"])

m.add_mod("vasp/5.4.1", preset="path", destination=prefix+"vasp.5.4.1/bin",
          depend=["mkl/13.0.079", "openmpi/1.10.0"])

m.add_mod("exciting/carbon", preset="path",
          destination=prefix+"exciting.carbon/bin",
          depend=["mkl/13.0.079", "openmpi/1.10.0"])

# for aipes
m.add_mod("anaconda3", preset="mod", destination=prefix+"anaconda3")
m.add_mod("amp/0.6", preset="py", destination=prefix+"amp-v0.6",
          depend=["anaconda3"])
m.add_mod("aipes", preset="py", destination=prefix+"aipes",
          depend=["anaconda3", "amp/0.6"])
