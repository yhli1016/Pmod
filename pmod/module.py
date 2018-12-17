import sys
import os
from pmod.utilities import print_stderr


class Module(object):
    """
    Class that represents a module.

    Each instance of this class has five lists, namely environ, depend,
    conflict, command and alias.

    self.environ contains the commands to set environmental variables.
    Each element in environ is a three-element tuple in the form (action, name,
    pattern), where action should be in ("append", "prepend", "reset"), name is
    the name of environmental on which the action will be modified, and pattern
    is the string with which the environmental variable will be modified.

    self.depend contains the dependencies of this module.

    self.conflict contains the conflicting modules.

    self.command contains additional initialization commands.

    self.alias contains the aliases to be set. Each element in alias is a tuple
    with two elements (alias name, alias string).
    """
    def __init__(self, mod_name, **kwargs):
        """
        :param mod_name: string, name of the module
        :param **kwargs: see the add_settings method of the Module class
        """
        self.mod_name = mod_name
        self.environ = [("prepend", "PM_LOADED_MODULES", self.mod_name)]
        self.depend = []
        self.conflict = []
        self.command = []
        self.alias = []
        self.add_settings(**kwargs)

    def add_settings(self, preset="void", destination=None, environ=None,
                     depend=None, conflict=None, command=None, alias=None):
        """
        Add settings to this instance.

        :param preset: string, preset elements to be added to self.environ,
                       should be in ("mod", "path", "lib", "inc", "py", "void")
        :param destination: string, installation destination of the module
        :param environ: list of tuples, see the documentation of 'Module' class
        :param depend: list of strings, dependencies of the module
        :param conflict: list of strings, conflicting modules of the module
        :param command: list of strings, additional initialization scripts
        :param alias: list of tuples, alias settings
        :return: None
        """
        # Add pre-defined items to environ
        if preset == "mod":
            self.environ.append(("prepend", "PATH", destination + "/bin"))
            self.environ.append(("prepend", "LIBRARY_PATH",
                                 destination + "/lib"))
            self.environ.append(("prepend", "LD_LIBRARY_PATH",
                                 destination + "/lib"))
            self.environ.append(("prepend", "C_INCLUDE_PATH",
                                 destination + "/include"))
            self.environ.append(("prepend", "CPLUS_INCLUDE_PATH",
                                 destination + "/include"))
        elif preset == "path":
            self.environ.append(("prepend", "PATH", destination))
        elif preset == "lib":
            self. environ.append(("prepend", "LIBRARY_PATH", destination))
            self.environ.append(("prepend", "LD_LIBRARY_PATH", destination))
        elif preset == "inc":
            self.environ.append(("prepend", "C_INCLUDE_PATH", destination))
            self.environ.append(("prepend", "CPLUS_INCLUDE_PATH", destination))
        elif preset == "py":
            self.environ.append(("prepend", "PYTHONPATH", destination))
        elif preset == "void":
            pass
        else:
            print_stderr("ERROR: undefined preset type %s" % preset)
            sys.exit(-1)

        # Add other items
        if environ is not None:
            self.environ.extend(environ)
        if depend is not None:
            self.depend.extend(depend)
        if conflict is not None:
            self.conflict.extend(conflict)
        if command is not None:
            self.command.extend(command)
        if alias is not None:
            self.alias.extend(alias)
        self.check_environ()

    def check_environ(self):
        """
        Check if there are undefined operations in self.environ

        :return: None
        """
        for environ_item in self.environ:
            if environ_item[0] not in ("append", "prepend", "reset"):
                print_stderr("ERROR: module %s has undefined operation %s"
                             % (self.mod_name, environ_item[0]))
                sys.exit(-1)

    def check_status(self):
        """
        Check the status of this module.

        :return: 1 for "loaded", 0 for "broken", -1 for "unloaded"
        """
        num_key_total = len(self.environ)
        num_key_set = 0
        for environ_item in self.environ:
            operation, env_name, pattern = environ_item[0], environ_item[1],\
                                           environ_item[2]
            if (operation == "reset"
                and env_name in os.environ.keys()
                and pattern in os.environ[env_name].split(":")):
                num_key_set += 1
            elif (operation in ("append", "prepend")
                  and env_name in os.environ.keys()
                  and pattern in os.environ[env_name].split(":")):
                num_key_set += 1
        if num_key_set == num_key_total:
            return 1
        elif num_key_set in range(1, num_key_total):
            return 0
        else:
            return -1

    def load(self, sandbox):
        """
        Update the environmental settings in sandbox to load this module.

        :param sandbox: instance of the SandBox class to collect settings from
                        this module
        :return: None
        """
        for environ_item in self.environ:
            operation, env_name, pattern = environ_item[0], environ_item[1],\
                                           environ_item[2]
            if operation == "reset":
                sandbox.reset_env(env_name, pattern)
            elif operation == "append":
                sandbox.append_env(env_name, pattern)
            elif operation == "prepend":
                sandbox.prepend_env(env_name, pattern)
        sandbox.add_alias(self.alias)
        sandbox.add_command(self.command)

    def unload(self, sandbox):
        """
        Update the environmental settings in sandbox to unload this module.

        :param sandbox: instance of the SandBox class to collect settings from
                        this module
        :return: None
        """
        for environ_item in self.environ:
            operation, env_name, pattern = environ_item[0], environ_item[1],\
                                           environ_item[2]
            if operation == "reset":
                sandbox.reset_env(env_name, "")
            elif operation in ("append", "prepend"):
                sandbox.remove_env(env_name, pattern)
        sandbox.add_unalias(self.alias)
