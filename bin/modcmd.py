#! /bin/env python
import argparse
from pmod.utilities import print_stderr
from pmod.config import mod_manager


# Parse cli-parameters
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--auto", default=False, action="store_true")
parser.add_argument("operation", type=str,  action="store")
parser.add_argument("mod_name", type=str, action="store", nargs="*")
args = parser.parse_args()

# Sanity check
mod_manager.check_sanity()
if args.operation in ("info", "show", "display", "diagnose", "probe",
                      "load", "add", "unload", "remove", "rm", "delete", "del"):
    mod_name = mod_manager.check_mod_names(args.mod_name)
else:
    mod_name = args.mod_name

# Perform the required operation
if args.operation in ("avail", "av"):
    mod_manager.print_available_mods()
elif args.operation in ("status", "stat"):
    mod_manager.print_mods_status()
elif args.operation in ("list", "ls"):
    mod_manager.print_mods_status(loaded_only=True)
elif args.operation in ("info", "show", "display"):
    mod_manager.print_mods_info(mod_name)
elif args.operation in ("diagnose", "probe"):
    mod_manager.diagnose_mods(mod_name)
elif args.operation in ("search",):
    mod_manager.search_mods(mod_name)
elif args.operation in ("load", "add"):
    mod_manager.load_mods(mod_name, args.auto)
elif args.operation in ("unload", "remove", "rm", "delete", "del"):
    mod_manager.unload_mods(mod_name, args.auto)
elif args.operation in ("clean", "purge"):
    mod_manager.unload_mods(mod_manager.get_mod_names())
else:
    print_stderr("Undefined operation %s" % args.operation)
