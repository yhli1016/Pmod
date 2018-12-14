from pmod.modmanager import ModManager
from modulefiles.foobar import FooBar

mod_manager = ModManager()
mod_manager.create_mod("test", mod_class=FooBar, preset="void")
