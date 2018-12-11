from pmod.module import Module
from pmod.utilities import print_stderr

class FooBar(Module):
    """
    A class with overrode 'load' and 'unload' method, for demonstrating custom
    loading and unloading procedures.
    """
    def load(self, sandbox):
        print_stderr("Loading module foobar!")
        super(FooBar, self).load(sandbox)

    def unload(self, sandbox):
        print_stderr("Unloading module foobar!")
        super(FooBar, self).unload(sandbox)