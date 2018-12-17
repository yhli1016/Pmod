import sys
import os
import re
from pmod.utilities import (print_stderr, print_banner, get_terminal_size,
                            print_table, print_list, get_latest_version)
from pmod.module import Module
from pmod.sandbox import SandBox


class ModManager(object):
    """
    The Module Manager class that receives the user's commands and perform
    specified operations.
    """
    def __init__(self):
        self.available_mods = dict()

    def create_mod(self, mod_name, mod_class=Module, **kwargs):
        """
        Create a new module to self.available_mods and initialize its items.
        If the module already exists, then add new items to this module.

        :param mod_name: string, name of the module
        :param mod_class: class object, type of the module to create if not
                          present
        :param kwargs: see the add_settings method of the Module class
        :return: None
        """
        if mod_name not in self.available_mods.keys():
            self.available_mods[mod_name] = mod_class(mod_name, **kwargs)
        else:
            self.available_mods[mod_name].add_settings(**kwargs)

    def add_mod(self, module):
        """
        Add an existing module to self.available_mods.

        :param module: instance of the 'Module' class and all derived classes
        :return: None
        """
        self.available_mods[module.mod_name] = module

    def check_sanity(self):
        """
        Check the sanity of modules defined in self.available_mods.

        :return: None
        """
        for mod_name, module in self.available_mods.items():
            module.check_environ()
            for depend_item in module.depend:
                if depend_item not in self.available_mods.keys():
                    print_stderr("ERROR: module %s has undefined dependency %s"
                                 % (mod_name, depend_item))
                    sys.exit(-1)
            for conflict_item in module.conflict:
                if conflict_item not in self.available_mods.keys():
                    print_stderr("ERROR: module %s has undefined conflicting"
                              " module %s" % (mod_name, conflict_item))
                    sys.exit(-1)
            if mod_name in self.build_dependencies([mod_name],
                                                   include_roots=False):
                print_stderr("ERROR: module %s has cyclic dependencies"
                             % mod_name)
                sys.exit(-1)

    def check_mod_names(self, mod_list):
        """
        Check if given modules have been defined in self.available_mods and
        return a list with the names of all defined modules. If the module name
        does not contain version number, then the last version number will be
        appended to it. If no matching module is found, then it is removed from
        mod_list and a warning message is casted.

        :param mod_list: list of the names of modules
        :return: list of the names of defined modules
        """
        mods_defined = []
        for mod_name in mod_list:
            # Search for all possible versions
            mods_found = []
            for mod_avail in self.available_mods.keys():
                if re.search(r"%s[-/]+[0-9\.]+.?" % mod_name, mod_avail,
                            re.IGNORECASE):
                    mods_found.append(mod_avail)
            if len(mods_found) != 0:
                mods_defined.append(get_latest_version(mods_found))
            else:
                # If no version is found, then search for the module name
                # directly.
                mods_found = []
                for mod_avail in self.available_mods.keys():
                    if re.search(r"%s" % mod_name, mod_avail, re.IGNORECASE):
                        mods_found.append(mod_avail)
                status_match = False
                for mod_found in mods_found:
                    if mod_name.lower() == mod_found.lower():
                        mods_defined.append(mod_found)
                        status_match = True
                if not status_match:
                    print_stderr("WARNING: undefined module %s skipped"
                                 % mod_name)
                    print_list("Suggestions", mods_found, number_items=False)
        return mods_defined

    def get_mod_names(self):
        """
        Get all the names of available modules.

        :return: list of the names of available modules
        """
        return self.available_mods.keys()

    def build_dependencies(self, root_mods, include_roots=True):
        """
        Extract the dependencies recursively for a list of modules.

        :param root_mods: list of the names of root modules
        :param include_roots: boolean, whether to include root mods in results
        :return: set of the names of all the dependencies
        """
        if include_roots:
            dependencies = [mod_name for mod_name in root_mods]
        else:
            dependencies = []
            for mod_name in root_mods:
                dependencies.extend(self.available_mods[mod_name].depend)
        for mod_name in dependencies:
            module = self.available_mods[mod_name]
            for depend_item in module.depend:
                if depend_item not in dependencies:
                    dependencies.append(depend_item)
        return set(dependencies)

    def build_conflicts(self, mod_list):
        """
        Extract the conflicting modules for a list of modules.

        :param mod_list: list of the names of modules
        :return: set of the names of all the conflicting modules
        """
        conflicts = []
        for mod_name in mod_list:
            module = self.available_mods[mod_name]
            conflicts.extend(module.conflict)
        return set(conflicts)

    def sort_mods(self, mod_list):
        """
        Sort modules according to their depth in the dependency tree.

        :param mod_list: list of modules to sort
        :return: sorted list with depth in decreasing order
        """
        # Build the dependency tree
        # It is assumed that the modules have been checked for cyclic
        # dependencies. Otherwise the loop will be INFINITE.
        depend_tree = [[mod_name, 0] for mod_name in mod_list]
        depth = 0
        status_updated = True
        while status_updated:
            status_updated = False
            nodes_to_check = [node for node in depend_tree if node[1] == depth]
            for parent in nodes_to_check:
                for child in depend_tree:
                    if child[0] in self.available_mods[parent[0]].depend:
                        child[1] += 1
                        status_updated = True
            depth += 1

        # Sort the nodes according to their depth in dependency tree
        sorted_tree = sorted(depend_tree, key=lambda x: x[1], reverse=True)
        sorted_mods = [node[0] for node in sorted_tree]
        return sorted_mods

    def auto_adjust_load(self, mods_to_unload, mods_to_load, mods_loaded):
        """
        Adjust the modules to unload and to load according to the status of
        already loaded modules when loading specified targets in automatic mode.
        The following operations are performed:

        1. Unusable modules due to conflicts with mods_to_load are added to
           mods_to_unload.
        2. Unusable modules due to dependency on mods_to_unload are added to
           mods_to_unload recursively.
        3. Modules that have to be reloaded due to conflicts with mods_to_unload
           are added to both lists.
        4. Modules that have to be reloaded due to dependencies on mods_to_load
           are added to both lists recursively.

        This piece of code may be the most complicated and bug-prone part of
        this software. So TEST CAREFULLY if you made any changes. Knowing
        exactly what you are doing is not enough, as programs often (always) do
        not work as you expect. In particular, DO NOT change the order of steps
        1-4 as they do not commute.

        :param mods_to_unload: list of strings, names of the modules to unload
        :param mods_to_load: list or strings, names of the modules to load
        :param mods_loaded: list of strings, names of loaded modules
        :return: adjusted mods_to_unload and mods_to_load
        """
        # Get the list of loaded modules that have to be checked for
        # usability.
        mods_loaded = set(mods_loaded)
        mods_loaded_copy = mods_loaded.copy()
        mods_loaded_copy = mods_loaded_copy.difference(set(mods_to_unload))
        mods_loaded_copy = mods_loaded_copy.union(set(mods_to_load))
        mods_check = mods_loaded.intersection(mods_loaded_copy)

        # Get the dependencies and conflicting modules of mods_check.
        dependencies = dict()
        conflicts = dict()
        for loaded_mod in mods_check:
            dependencies[loaded_mod] = self.build_dependencies([loaded_mod])
            conflicts[loaded_mod] = self.build_conflicts(
                                    dependencies[loaded_mod])

        # 1. Check for unusable modules due to conflicts with mods_to_load.
        mods_check_copy = mods_check.copy()
        for mod_name in mods_to_load:
            for loaded_mod in mods_check:
                if (mod_name in conflicts[loaded_mod]
                    and loaded_mod not in mods_to_unload):
                    mods_to_unload.append(loaded_mod)
                    mods_check_copy.remove(loaded_mod)
        mods_check = mods_check_copy

        # 2. Check for unusable modules due to dependency on mods_to_unload
        # recursively.
        mods_check_copy = mods_check.copy()
        for mod_name in mods_to_unload:
            for loaded_mod in mods_check:
                if (mod_name in dependencies[loaded_mod]
                    and loaded_mod not in mods_to_unload):
                    mods_to_unload.append(loaded_mod)
                    mods_check_copy.remove(loaded_mod)
        mods_check = mods_check_copy

        # 3. Check for modules that have to be reloaded due to conflicts on
        # mods_to_unload.
        mods_check_copy = mods_check.copy()
        mods_to_reload = []
        for mod_name in mods_to_unload:
            for loaded_mod in mods_check:
                if (mod_name in conflicts[loaded_mod]
                    and loaded_mod not in mods_to_reload):
                    mods_to_reload.append(loaded_mod)
                    mods_check_copy.remove(loaded_mod)
        mods_to_load.extend(mods_to_reload)
        mods_to_unload.extend(mods_to_reload)
        mods_check = mods_check_copy

        # 4. Check for modules that have to be reloaded due to dependency on
        # mods_to_load recursively.
        for mod_name in mods_to_load:
            for loaded_mod in mods_check:
                if (mod_name in dependencies[loaded_mod]
                    and loaded_mod not in mods_to_load):
                    mods_to_load.append(loaded_mod)
                    mods_to_unload.append(loaded_mod)

        return set(mods_to_unload), set(mods_to_load)

    def auto_adjust_unload(self, mods_to_unload, mods_to_load, mods_loaded):
        """
        Adjust the modules to unload and to load according to the status of
        already loaded modules when unloading specified targets in automatic
        mode. The following operations are performed:

        1. Modules that are still required by other loaded modules are excluded
           from mods_to_unload. If all the modules are required, then nothing
           will be unloaded.
        2. Unusable modules due to dependency on mods_to_unload are added to
           mods_to_unload recursively.
        3. Modules that have to be reloaded due to conflicts with mods_to_unload
           are added to both lists.
        4. Modules that have to be reloaded due to dependencies on mods_to_load
           are added to both lists recursively.

        Step 2-4 are identical to that in the 'auto_adjust_load' method. For the
        same reason test carefully if you change this piece of code.

        :param mods_to_unload: list of strings, names of the modules to unload
        :param mods_to_load: list or strings, names of the modules to load
        :param mods_loaded: list of strings, names of loaded modules
        :return: adjusted mods_to_unload and mods_to_load
        """
        # Get the loaded modules to be checked and their dependencies and
        # conflicts.
        mods_loaded = set(mods_loaded)
        mods_check = mods_loaded.difference(set(mods_to_unload))
        dependencies = dict()
        conflicts = dict()
        for loaded_mod in mods_check:
            dependencies[loaded_mod] = self.build_dependencies([loaded_mod])
            conflicts[loaded_mod] = self.build_conflicts(
                                    dependencies[loaded_mod])

        # 1. Check for modules in mods_to_unload that are still required by
        # modules in mods_check.
        mods_in_use = set()
        for mod_name in mods_to_unload:
            in_use = False
            for loaded_mod in mods_check:
                if mod_name in dependencies[loaded_mod]:
                    in_use = True
            if in_use:
                mods_in_use.add(mod_name)
        mods_to_unload = list(set(mods_to_unload).difference(mods_in_use))

        # 2. Check for unusable modules due to dependency on mods_to_unload
        # recursively.
        mods_check_copy = mods_check.copy()
        for mod_name in mods_to_unload:
            for loaded_mod in mods_check:
                if (mod_name in dependencies[loaded_mod]
                    and loaded_mod not in mods_to_unload):
                    mods_to_unload.append(loaded_mod)
                    mods_check_copy.remove(loaded_mod)
        mods_check = mods_check_copy

        # 3. Check for modules that have to be reloaded due to conflicts on
        # mods_to_unload.
        mods_check_copy = mods_check.copy()
        mods_to_reload = []
        for mod_name in mods_to_unload:
            for loaded_mod in mods_check:
                if (mod_name in conflicts[loaded_mod]
                    and loaded_mod not in mods_to_reload):
                    mods_to_reload.append(loaded_mod)
                    mods_check_copy.remove(loaded_mod)
        mods_to_load.extend(mods_to_reload)
        mods_to_unload.extend(mods_to_reload)
        mods_check = mods_check_copy

        # 4. Check for modules that have to be reloaded due to dependency on
        # mods_to_load recursively.
        for mod_name in mods_to_load:
            for loaded_mod in mods_check:
                if (mod_name in dependencies[loaded_mod]
                    and loaded_mod not in mods_to_load):
                    mods_to_load.append(loaded_mod)
                    mods_to_unload.append(loaded_mod)

        return set(mods_to_unload), set(mods_to_load)

    def print_available_mods(self):
        """
        Print all available modules.

        :return: None
        """
        mod_names = sorted(self.available_mods.keys(), key=str.lower)
        print_table("Available Modules", mod_names, number_items=False)

    def print_mods_status(self, loaded_only=False):
        """
        Print the status of all available modules.

        :param loaded_only: boolean, whether to list loaded modules only
        :return: None
        """
        mods_loaded = []
        mods_broken = []
        mods_unloaded = []

        for mod_name, module in self.available_mods.items():
            mod_status = module.check_status()
            if mod_status == 1:
                mods_loaded.append(mod_name)
            elif mod_status == 0:
                mods_broken.append(mod_name)
            else:
                mods_unloaded.append(mod_name)
        mods_loaded = sorted(mods_loaded, key=str.lower)
        mods_broken = sorted(mods_broken, key=str.lower)
        mods_unloaded = sorted(mods_unloaded, key=str.lower)

        print_table("Loaded Modules", mods_loaded)
        if len(mods_broken) != 0:
            print_table("Broken Modules", mods_broken)
        if not loaded_only:
            print_table("Unloaded Modules", mods_unloaded)

    def print_mods_info(self, mod_list):
        """
        Print the dependencies and conflicting modules of given modules in
        mod_list.

        :param mod_list: list of module names
        :return: None
        """
        num_row, num_column = get_terminal_size()
        for mod_name in mod_list:
            module = self.available_mods[mod_name]
            print_table("Module", [mod_name], number_items=False)

            # Print module.environ
            print_banner("Environ", num_column)
            max_length = max([len(env[1]) for env in module.environ])
            fmt = "%-8s %-" + str(max_length) + "s %s"
            for env in module.environ:
                print_stderr(fmt % (env[0], env[1], env[2]))

            # Print dependencies, conflicting modules and commands
            print_table("Dependencies", module.depend, number_items=False)
            print_table("Conflicting modules", module.conflict,
                        number_items=False)
            print_table("Commands", module.command, number_items=False)

            # Print aliases
            print_banner("Aliases", num_column)
            if len(module.alias) != 0:
                fmt = "alias %s=\"%s\""
                for alias in module.alias:
                    print_stderr(fmt % (alias[0], alias[1]))
                print_stderr("")
            else:
                print_stderr("None\n")

    def diagnose_mods(self, mod_list):
        """
        Check if the dependencies have been loaded and if conflicting modules
        have been unloaded for a list of given modules.

        :param mod_list: list of strings, names of modules to check
        :return: None
        """
        num_row, num_column = get_terminal_size()
        for mod_name in mod_list:
            module = self.available_mods[mod_name]
            print_table("Module", [mod_name], number_items=False)

            # Check module.environ
            print_banner("Environ", num_column)
            environ = module.environ
            status = True
            for environ_item in environ:
                operation, env_name, pattern = environ_item[0], \
                                               environ_item[1], environ_item[2]
                if (operation == "reset"
                    and not (env_name in os.environ.keys()
                             and os.environ[env_name] == pattern)):
                    print_stderr("WARNING: %s not set" % env_name)
                    status = False
                elif (operation in ("append", "prepend")
                      and not (env_name in os.environ.keys()
                               and pattern in os.environ[env_name].split(":"))):
                    print_stderr("WARNING: %s not set" % env_name)
                    status = False
            if status:
                print_stderr("OK")
            print_stderr("")

            # Check dependencies
            print_banner("Dependencies", num_column)
            dependencies = self.build_dependencies([mod_name],
                                                    include_roots=False)
            status = True
            for depend_item in dependencies:
                if self.available_mods[depend_item].check_status() != 1:
                    print_stderr("WARNING: %s not loaded" % depend_item)
                    status = False
            if status:
                print_stderr("OK")
            print_stderr("")

            # Check conflicts
            print_banner("Conflicting modules", num_column)
            conflicts = self.build_conflicts([mod_name])
            status = True
            for conflict_item in conflicts:
                if self.available_mods[conflict_item].check_status() != -1:
                    print_stderr("WARNING: %s not unloaded" % conflict_item)
                    status = False
            if status:
                print_stderr("OK")
            print_stderr("")

    def search_mods(self, pattern_list):
        """
        Search for modules matching the patterns.

        :param pattern_list: list of strings, pattern to be matched against
        :return: None
        """
        for pattern in pattern_list:
            try:
                mods_found = [mod_name for mod_name in self.available_mods.keys()
                              if re.search(pattern, mod_name, re.IGNORECASE)
                              is not None]
                print_table("Modules matching %s" % pattern, mods_found,
                            number_items=False)
            except re.error:
                print_stderr("Invalid regular expression %s" % pattern)

    def load_mods(self, mod_list, force_no_auto=False, auto=False):
        """
        Load a list of modules.

        :param mod_list: list of the names of modules
        :param force_no_auto: boolean, whether to force to disable auto mode,
                              overwrites auto and PM_AUTO_MODE
        :param auto: boolean, whether to enable auto mode
        :return: None
        """
        if force_no_auto or (not auto and os.environ['PM_AUTO_MODE'] != "1"):
            mods_to_load = set([mod_name for mod_name in mod_list
                        if self.available_mods[mod_name].check_status() != 1])
            mods_to_unload = set()
        else:
            # Check if there are paradoxes
            dependencies = self.build_dependencies(mod_list)
            conflicts = self.build_conflicts(dependencies)
            mods_paradox = dependencies.intersection(conflicts)
            if len(mods_paradox) != 0:
                for mod_name in mods_paradox:
                    print_stderr("ERROR: module %s is claimed to be both "
                                 "dependency and conflicting module" % mod_name)
                sys.exit(-1)

            # Reload broken modules to simplify the logic flow and to avoid
            # potential bugs
            mods_unloaded = []
            mods_broken = []
            mods_loaded = []
            for mod_name, module in self.available_mods.items():
                status = module.check_status()
                if status == -1:
                    mods_unloaded.append(mod_name)
                elif status == 0:
                    mods_broken.append(mod_name)
                else:
                    mods_loaded.append(mod_name)
            if len(mods_broken) != 0:
                self.unload_mods(mods_broken, force_no_auto=True)
                self.load_mods(mods_broken, force_no_auto=True)
                mods_loaded.extend(mods_broken)

            # Get the lists of modules to unload and to load
            mods_to_unload = [mod_name for mod_name in conflicts
                              if mod_name not in mods_unloaded]
            mods_to_load = [mod_name for mod_name in dependencies
                            if mod_name not in mods_loaded]
            mods_to_unload, mods_to_load = self.auto_adjust_load(mods_to_unload,
                                                      mods_to_load, mods_loaded)

        # Collect settings from each module and echo
        mods_to_unload = self.sort_mods(mods_to_unload)
        mods_to_load = self.sort_mods(mods_to_load)
        sandbox = SandBox()
        for mod_name in mods_to_unload:
            self.available_mods[mod_name].unload(sandbox)
        for mod_name in mods_to_load:
            self.available_mods[mod_name].load(sandbox)
        sandbox.echo_commands()

    def unload_mods(self, mod_list, force_no_auto=False, auto=False):
        """
        Unload specified list of modules with their dependencies that are not.

        :param mod_list: list of the names of modules
        :param force_no_auto: boolean, whether to force to disable auto mode,
                              overwrites auto and PM_AUTO_MODE
        :param auto: boolean, whether to enable auto mode
        :return: None
        """
        if force_no_auto or (not auto and os.environ['PM_AUTO_MODE'] != "1"):
            mods_to_unload = set([mod_name for mod_name in mod_list
                        if self.available_mods[mod_name].check_status() != -1])
            mods_to_load = set()
        else:
            # Reload broken modules to simplify the logic flow and to avoid
            # potential bugs
            mods_unloaded = []
            mods_broken = []
            mods_loaded = []
            for mod_name, module in self.available_mods.items():
                status = module.check_status()
                if status == -1:
                    mods_unloaded.append(mod_name)
                elif status == 0:
                    mods_broken.append(mod_name)
                else:
                    mods_loaded.append(mod_name)
            if len(mods_broken) != 0:
                self.unload_mods(mods_broken, force_no_auto=True)
                self.load_mods(mods_broken, force_no_auto=True)
                mods_loaded.extend(mods_broken)

            # Get the list of modules to unload and to load
            dependencies = self.build_dependencies(mod_list)
            mods_to_unload = [mod_name for mod_name in dependencies
                              if mod_name not in mods_unloaded]
            mods_to_load = []
            mods_to_unload, mods_to_load = self.auto_adjust_unload(
                                      mods_to_unload, mods_to_load, mods_loaded)

        # Collect settings from each module and echo
        mods_to_unload = self.sort_mods(mods_to_unload)
        mods_to_load = self.sort_mods(mods_to_load)
        sandbox = SandBox()
        for mod_name in mods_to_unload:
            self.available_mods[mod_name].unload(sandbox)
        for mod_name in mods_to_load:
            self.available_mods[mod_name].load(sandbox)
        sandbox.echo_commands()

    def reload(self):
        """
        Reload all loaded and broken modules.

        :return: None
        """
        mods_to_load = [mod_name for mod_name in self.available_mods.keys()
                        if self.available_mods[mod_name].check_status() != -1]
        mods_to_load = self.sort_mods(mods_to_load)
        sandbox = SandBox()
        for mod_name in mods_to_load:
            self.available_mods[mod_name].unload(sandbox)
        for mod_name in mods_to_load:
            self.available_mods[mod_name].load(sandbox)
        sandbox.echo_commands()
