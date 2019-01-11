from pmod.module import Module


def exclude(items, item_excluded):
    items_remain = [item for item in items if item != item_excluded]
    return items_remain


mpi_versions = ['IntelMPI/2018.1.163', 'openmpi/3.1.3-intel',
                'openmpi/2.0.2-gcc', 'openmpi/1.6.5-gcc']


class IntelCCDer(Module):
    def __init__(self, mod_name, **kwargs):
        super(IntelCCDer, self).__init__(mod_name, **kwargs)
        self.depend.append('IntelCC/2018.1.163')


class IntelMPI(IntelCCDer):
    def __init__(self, mod_name, **kwargs):
        super(IntelMPI, self).__init__(mod_name, **kwargs)
        self.conflict.extend(exclude(mpi_versions, 'IntelMPI/2018.1.163'))


class IntelMPIDer(IntelMPI):
    def __init__(self, mod_name, **kwargs):
        super(IntelMPIDer, self).__init__(mod_name, **kwargs)
        self.depend.append('IntelMPI/2018.1.163')


class OpenMPI165(Module):
    def __init__(self, mod_name, **kwargs):
        super(OpenMPI165, self).__init__(mod_name, **kwargs)
        self.conflict.extend(exclude(mpi_versions, 'openmpi/1.6.5-gcc'))


class OpenMPI165Der(OpenMPI165):
    def __init__(self, mod_name, **kwargs):
        super(OpenMPI165Der, self).__init__(mod_name, **kwargs)
        self.depend.append('openmpi/1.6.5-gcc')


class OpenMPI202(Module):
    def __init__(self, mod_name, **kwargs):
        super(OpenMPI202, self).__init__(mod_name, **kwargs)
        self.conflict.extend(exclude(mpi_versions, 'openmpi/2.0.2-gcc'))


class OpenMPI202Der(OpenMPI202):
    def __init__(self, mod_name, **kwargs):
        super(OpenMPI202Der, self).__init__(mod_name, **kwargs)
        self.depend.append('openmpi/2.0.2-gcc')


class OpenMPI313(IntelCCDer):
    def __init__(self, mod_name, **kwargs):
        super(OpenMPI313, self).__init__(mod_name, **kwargs)
        self.conflict.extend(exclude(mpi_versions, 'openmpi/3.1.3-intel'))


class OpenMPI313Der(OpenMPI313):
    def __init__(self, mod_name, **kwargs):
        super(OpenMPI313Der, self).__init__(mod_name, **kwargs)
        self.depend.append('openmpi/3.1.3-intel')