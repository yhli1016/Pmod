# Installation destination of pmod
PM_ROOT=$HOME/proj/pmod

# Setup environment variables
export PATH=$PM_ROOT/bin:$PATH
export PYTHONPATH=$PM_ROOT:$PYTHONPATH
export PM_LOADED_MODULES=""

# Setup the 'module' command
if [ ! -x "$PM_ROOT/bin/modcmd.py" ]; then
    chmod +x $PM_ROOT/bin/modcmd.py
fi
function module ()
{
    eval `modcmd.py $*`
}

commands="avail av status stat list ls info show display diagnose probe search \
load add unload remove rm delete del clean purge reload update"
complete -W "$commands" module
