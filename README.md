About
-----
Pmod is a light-weight environment module system written in Python. Initially it
came out as the successor of a complicated shell script for managing
user-dependent environmental variables. As shell script was not well suited for
such tasks, and we did not have enough time to deploy and learn advanced module
systems like Lmod, we decided to write our own module system.

Pmod is designed with simplicity in mind and implemented in an intuitive
objected-oriented manner. Of course, the limits of our knowledge and programming
skills prohibit the possibility of creating an advanced environment module
system as we are students majoring in physics, not computers. Installation of
pmod is very easy. No prerequisites are required besides Python. Root privileges
are not required if pmod is not to be installed for all users. Configuration of
pmod requires some basic Python knowledge.

Despite its simplicity, the basic capabilities of a common module system are
supported, such as listing available and loaded modules, obtaining the module
status, loading and unloading modules with automatic prerequisites and
conflicting modules resolving, diagnosis on module usability, searching for
given modules and printing their configuration details. New features may be
added as we have more user experience in actual applications, e.g. support for
other shells in addition to bash.


Install
-------
Pmod does not have any other dependencies except Python. Both Python 2 and
Python 3 are supported. The common installation procedure is as below:

1. Copy all files and directories to the installation destination, e.g.
   ~/soft/pmod. If you plan to install pmod for all the users, we suggest
   /opt/pmod as the installation destination. Note that in this case root
   privileges will be required.

2. Edit init/bash.sh to update PM\_ROOT to the installation destination of pmod
   in step 1.

3. Add the command to source init/bash.sh in your ~/.bashrc. If pmod is to be
   installed for all the users, copy init/bash.sh to /etc/profile.d or source it
   in /etc/profile. The latter is recommended.

4. Ordinary users may not have the privileges to generate \*.pyc files outside
   their home directory. In that case, load each python environment (e.g.
   different versions of Anaconda) and type 'module list' to generate these
   files in advance.


Configuration
-------------
Configurations of available modules are stored in pmod/config.py as an instance
of the *ModManager* class. bin/modcmd.py then imports this instance and call its
methods to perform specified operations. Inside this class a dictionary named
*available\_mods* contained all the module definitions.

Each module is presented with an instance of the *Module* class, which has five
lists: *environ*, *depend*, *conflict*, *command* and "alias". Each element of
*environ* is a tuple with three elements: action to be performed, name of the
environmental variable, and the string with which the environmental variable
will be modified. Modules can have dependencies, conflicting modules,
additional initialization scripts and aliases settings, as stored in the lists
of *depend*, *conflict*, *command* and *alias* respectively. Each element of
*alias* is a tuple of (alias name, alias string).

The auxiliary method *add\_mod()* of *ModManager* is provided for the
manipulation of modules, which calls the *add\_settings()* method of *Module*.
A set of predefined elements to self.environ can be added automatically
according to the *preset* argument, which should be in "mod", "path", "lib",
"inc", "py",  and "void". Sub-directories like "bin", "lib" and "included" are
deduced automatically when preset is set to "mod", but not in other cases.
Setting preset to "void" will create an empty module without any predefined
elements. Empty modules are useful when creating a collection of many modules,
with all the members claimed as dependencies. You can also modify
*available\_mods* directly if you prefer.

See pmod/config.py and pmod/modmanager.py for more details. Two configuration
files on our servers are provided in the *examples* directory.


Usage
-----
The common usage of pmod is "pmod [-a] operation [mod\_name...]". '-a' enables
automatic mode, which we will describe in more details. For now the supported
operations are:

- avail, av: list all available modules

- status, stat: print the status of modules

- list, ls: list all loaded modules

- info, show, display: show configuration details of specified modules

- diagnose, probe: check for usability of specified modules

- search: search for modules matching given pattern, with regular expressions
          support

- load, add: load specified modules

- unload, remove, rm, delete, del: unload specified modules

- clean, purge: unload all modules

- reload, update: reload all loaded modules

See modcmd.py for more details.


Automatic mode
--------------
You may find that pmod may not behave as you expect. For example, loading module
a will load not only this module itself, but also all of its prerequisites.
Moreover, many other modules may be unloaded even if you did not perform any
such operations. Unloading a specified module might 'fail' as nothing happens
actually. These abnormalities are caused by the 'automatic mode'.

Generally speaking, in automatic mode all the loaded modules must be usable. If
a module is not usable, then it should be removed from the loaded modules. For
that purpose, the following operations are triggered when loading specified
targets:

1. Prerequisites of the targets are loaded.
2. Conflicting modules of the targets are unloaded.
3. Unusable modules due to conflicts with modules to load are unloaded.
4. Unusable modules due to dependency on modules to unload are unloaded.
5. Modules that have conflicts with modules to unload are reloaded.
6. Modules that have dependencies on modules to load are reloaded.

When unloading specified targets, the following operations are triggered:

1. Prerequisites of the targets that are not required by any loaded modules are
   unloaded.
2. Unusable modules due to dependency on modules to unload are unloaded.
3. Modules that have conflicts with modules to unload are reloaded.
4. Modules that have dependencies on modules to load are reloaded.

The automatically mode are enabled by either appending '-a' or '--auto' to the
command-line parameters, or setting the PM\_AUTO\_MODE environmental variable to 1
in init/bash.sh. By default it is enabled. Set PM\_AUTO\_MODE to 0 if you don't
like this feature. Keep in mind that the loaded modules may be not usable as it
seems to be in this case.


FAQ (in advance)
----------------
Q: Why not separate configuration files into different files organized in many
   directories like that in lmod?

A: Doing so will increase the complexity of designing and using this software.
   Moreover, the package management mechanism of Python does not allow
   additional periods ('.') in the file name. So if version is to be included in
   configuration file names, the periods have to be replaced with underscores
   ('\_'). We don't think it a big problem to include all the configurations in
   one python file if the number of modules to manage is lower than 100. If you
   do have a lot of modules, and do not like a large configuration file, we
   recommend you the professional environmental module systems like Lmod.

Q: How about version management?

A: Version management is supported by pmod, but not directly. For example, if
   module foo has three versions, namely A, B and C, then in the definition of
   foo/A you should declare foo/B and foo/C as conflicting modules. For the
   definition of foo/B and foo/C, declare the other versions as conflicting
   modules mutually. It will not take much effort using list comprehension or
   set difference. Switching between different versions is as simple as invoking
   'module -a load module/B'.

Q: How can I define a meta-module that loads a collection of other modules?

A: Define it as a void module and add all the modules to load as dependencies.
