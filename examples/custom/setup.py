from pmod.config.foobar import FooBar
from pmod.modmanager import ModManager

mod_manager = ModManager()
mod_manager.add_mod("test", mod_class=FooBar, preset="void")