import os
from pmod.utilities import print_stdout


class SandBox(object):
    """
    Class that records the settings of each module and outputs shell commands
    to stdout.

    self.environ is a copy of os.environ, but has all the elements split by ":".

    self.env_name_changed records the environmental variables modifed by the
    modules to load or unload.

    self.command, self.alias and self.unalias records the command and alias of
    each module.
    """
    def __init__(self):
        self.environ = dict()
        for env_name, env_value in os.environ.items():
            self.environ[env_name] = env_value.split(":")
        self.env_name_changed = []
        self.command = []
        self.alias = []
        self.unalias = []

    def has_pattern(self, env_name, pattern):
        """
        Check if pattern is already included in self.environ[env_name].

        :param env_name: string, name of the environmental variable
        :param pattern: string, pattern to check
        :return: True if pattern already included, False otherwise.
        """
        if env_name not in self.environ.keys():
            return False
        else:
            return pattern in self.environ[env_name]

    def reset_env(self, env_name, pattern):
        """
        Reset the value of environmental variable.

        :param env_name: string, name of the environmental variable
        :param pattern: string, new value of environmental variable
        :return: None
        """
        self.environ[env_name] = [pattern]
        if env_name not in self.env_name_changed:
            self.env_name_changed.append(env_name)

    def append_env(self, env_name, pattern):
        """
        Append pattern to environmental variable.

        :param env_name: string, name of the environmental variable
        :param pattern: string, with which the environmental variable will be
                        modified
        :return: None
        """
        if not self.has_pattern(env_name, pattern):
            if env_name not in self.environ.keys():
                self.environ[env_name] = [pattern]
            else:
                self.environ[env_name].append(pattern)
            if env_name not in self.env_name_changed:
                self.env_name_changed.append(env_name)

    def prepend_env(self, env_name, pattern):
        """
        Prepend pattern to environmental variable.

        :param env_name: string, name of the environmental variable
        :param pattern: string, with which the environmental variable will be
                        modified
        :return: None
        """
        if not self.has_pattern(env_name, pattern):
            if env_name not in self.environ.keys():
                self.environ[env_name] = [pattern]
            else:
                self.environ[env_name].insert(0, pattern)
            if env_name not in self.env_name_changed:
                self.env_name_changed.append(env_name)

    def remove_env(self, env_name, pattern):
        """
        Remove pattern from environmental variable.

        :param env_name: string, name of the environmental variable
        :param pattern: string, pattern to be removed from the environmental
                        variable
        :return: None
        """
        if self.has_pattern(env_name, pattern):
            while pattern in self.environ[env_name]:
                self.environ[env_name].remove(pattern)
            if env_name not in self.env_name_changed:
                self.env_name_changed.append(env_name)

    def add_alias(self, alias):
        """
        Add aliases to be set to self.alias.

        :param alias: list of tuples, similar to that of Module class.
        :return: None.
        """
        self.alias.extend(alias)

    def add_unalias(self, unalias):
        """
        Add unaliases to self.unalias.

        :param unalias: list of tuples, similar to that of Module class.
        :return: None
        """
        self.unalias.extend(unalias)

    def add_command(self, command):
        """
        Add command to self.command.

        :param command: list of commands, similar to that of Module class.
        :return: None
        """
        self.command.extend(command)

    def echo_commands(self, shell="bash"):
        """
        Print shell commands to stdout to be evaluated by shell.

        :param shell: string, type of the shell that evaluates the output.
        :return: None
        """
        for env_name in self.env_name_changed:
            env_value = self.environ[env_name]
            env_string = "".join(["%s:" % pattern for pattern in env_value])
            while env_string != "" and env_string[-1] == ":":
                env_string = env_string[:-1]
            if shell == "bash":
                print_stdout("export %s=%s;" % (env_name, env_string))
            else:
                raise NotImplementedError("Shell type %s not supported" % shell)
        if shell == "bash":
            for alias in self.unalias:
                print_stdout("unalias %s;" % alias[0])
            for alias in self.alias:
                print_stdout("alias %s=\"%s\";" % (alias[0], alias[1]))
        for command in self.command:
            print_stdout("%s;" % command)