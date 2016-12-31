#!/bin/bash
#
# refresh_environments.sh
#
# USAGE: refresh__environments.sh conda_env1 [conda_env2, ...]
#
# This script will "refresh" the specified conda environments by
# first deleting each environment then re-creating it based on
# an environment file with the same name in this directory.
# For example if you have an environment named "myenv", with a
# corresponding myenv-environment.yml file specifying certain versions
# of certain packages, running refresh_environments.sh myenv
# will delete the myenv environment then re-create it with
# the package versions specified in myenv-environment.yml. This is
# useful if you've modified the environment in any way (say by
# installing, updating, or removing packages) and you want to
# restore the environment to its earlier state. Basically, it
# just saves you the work of typing a bunch of tedious "conda env"
# commands.
#
# WARNING - doing these things will cause problems:
# 1. Specifying an environment that doesn't exist.
# 2. Specifying an environment that doesn't have a corresponding
#    environment file (e.g. myenv-environment.yml)

if [ "$#" -lt 1 ]; then
    echo "You must specify at least one conda environment to refresh."
    echo "USAGE: refresh_environments.sh conda_env1 [conda_env2, ...]"
    exit 1
fi

for conda_env in "$@"; do
    conda env remove -n $conda_env -y -q
    conda env create -q -f $conda_env-environment.yml
done
