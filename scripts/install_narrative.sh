#!/usr/bin/env bash

# given a virtual environment, install jupyter notebook, and the KBase goodies on top
# 1. source into virtualenv
# > virtualenv narrative-jupyter
# > source narrative-jupyter/bin/activate
#
# 2. fetch the right tag of jupyter notebook
# > git clone https://github.com/jupyter/notebook jupyter-notebook
# > cd jupyter-notebook
# > git checkout tags/4.0.5
#
# 3. do the install
# > pip install --pre -e .
#
# > get clone https://github.com/ipython/ipywidgets
# > cd ipywidgets
# > git checkout tags/4.0.3
# > pip install -e .
#
# 4. setup configs to be in kbase-config, not in /home/users/.jupyter
# > SOME ENV VAR setup
#
# 5. go into src and grab requirements
# > cd src
# > pip install -r requirements.txt
#
# 6. install kbase stuff
# > python setup.py install
#
# 7. build run script. (see jupyter-narrative.sh)
# > cp jupyter-narrative.sh narrative-jupyter/bin
#
# 8. Done!

JUPYTER_NOTEBOOK_INSTALL_DIR=jupyter_notebook
JUPYTER_NOTEBOOK_REPO=https://github.com/jupyter/notebook
JUPYTER_NOTEBOOK_TAG=5.4.1

SCRIPT_TGT="kbase-narrative"

CUR_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
NARRATIVE_ROOT_DIR=$CUR_DIR/..
SCRIPT_TEMPLATE=$CUR_DIR/start_local_narrative.tmpl

# clear log
logfile=`pwd`/install.log
cat /dev/null > $logfile

function log () {
    now=`date '+%Y-%m-%d %H:%M:%S'`
    echo "$now [install_narrative] $1" | tee -a $logfile
}

function console () {
    now=`date '+%Y-%m-%d %H:%M:%S'`
    echo "$now [install_narrative] $1"
}

function usage () {
    printf "usage: $0 [options]\n"
    printf "options:\n"
    printf "  {-h | --help} \n\tShow these help options.\n"
    printf "  {-u | --update} \n\tUpdate the build only. Use this if you made updates to the source code and want to see your changes.\n"
}

# Arg parsing
# -----------

update_only=0
travis=0
while [ $# -gt 0 ]; do
    case $1 in
        -h | --help | -\?)
            usage
            exit 0
            ;;
        -u | --update)
            update_only=1
            shift
            ;;
        --travis)
            travis=1
            shift
            ;;
    esac
done

console "Install: complete log in: $logfile"

# Detect virtualenv
# ----------------
if [[ "x$CONDA_DEFAULT_ENV" = x ]] && [[ "x$VIRTUAL_ENV" = x ]] && [[ ! $no_venv -eq 1 ]]
then
  console 'ERROR: No virtual environment detected! Please activate one first.
  The easiest way to use virtual environments is with a Conda virtual environment.
  Activate your env with: conda activate kbase-narrative
  Narrative setup guide: https://github.com/kbase/narrative#setup
  Conda installation: https://conda.io/docs/user-guide/install/index.html'
  exit 1
fi

if [ ! $update_only -eq 1 ]
then
    # Install JavaScript packages
    # ---------------------------
    cd $NARRATIVE_ROOT_DIR
    npm install 2>&1 | tee -a ${logfile}
    bower install -V --allow-root --config.interactive=false 2>&1 | tee -a ${logfile}
fi

# Install Narrative code
# ----------------------
console "Installing biokbase modules"
log "Installing requirements from src/requirements.txt with 'pip'"
pip install -r src/requirements.txt 2>&1 | tee -a ${logfile}
if [ $? -ne 0 ]; then
    console "pip install for biokbase requirements failed: please examine $logfile"
    exit 1
fi
log "Running local 'setup.py'"
${PYTHON} src/setup.py install 2>&1 | tee -a ${logfile}
log "Done installing biokbase."

if [ ! $update_only -eq 1 ]
then
    # Setup jupyter_narrative script
    # ------------------------------
    console "Installing scripts"
    i=0
    while read s
        do
            echo $s
            if [ $i = 0 ]
                then
                echo d=`pwd`
                echo e=$(dirname `which python`)
                i=1
            fi
    done < $SCRIPT_TEMPLATE > $SCRIPT_TGT
    d=$(dirname `which python`)
    chmod 0755 $SCRIPT_TGT
    log "Putting new $SCRIPT_TGT command under $d"
    /bin/mv $SCRIPT_TGT $d
    log "Done installing scripts"

    log "Installing nbextensions"
    cd nbextensions
    sh install.sh
    cd ../..
    jupyter nbextension enable --py --sys-prefix widgetsnbextension
    log "Done installing nbextensions"
fi

console "Done. Run the narrative from your virtual environment with the command: $SCRIPT_TGT"
