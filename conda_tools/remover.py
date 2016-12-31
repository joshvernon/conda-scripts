#!/usr/bin/env python
#
# remover.py
#
# Changelog
# <Date>          <Description>
#  02-08-2016      Changed subprocess.Popen() to write stdout to a pipe
#                  instead of a file on disk.
#
#  02-08-2016      Changed regex to search for any non-whitespace character,
#                  followed by a hyphen("-"), followed by number.
#                  This is to account for numbers and hyphens in package names
#                  (e.g. "enum34" or "logilab-common").
#
#  11-29-2016      Changed module name to remover.py.
#                  Added call to utils.get_root_prefix().
#
# TODO : Create a better regex to get more packages.

import json
import os.path
import re
import shlex
import subprocess

import conda_api

from utils import get_root_prefix

def remove_package_with_dependencies(environment, package):
    # Before we do anything, set the ROOT_PREFIX
    # variable so conda_api knows where to work from.
    conda_api.set_root_prefix(get_root_prefix())

    # Set the name of the temporary conda environment
    # we'll work in.
    temp_env = 'temp_env'

    # Create the temporary environment in which to do our install test.
    conda_api.create(temp_env, pkgs=['python'])

    # Do a fake install of the package we want to remove,
    # in order to get its "dependencies".
    install_cmd = shlex.split('{0} install -n {1} {2} --json --dry-run'
                              .format(os.path.join(conda_api.ROOT_PREFIX, 'bin/conda'),
                                      temp_env, package))
    p = subprocess.Popen(install_cmd, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    install_response = json.loads(stdout)

    # Get the dependencies from the JSON that was written
    # by the conda install command above.
    regex = re.compile('\S*(?=-[0-9]+)')
    packages_to_remove = [regex.match(item.split(' ')[0]).group()
                          for item in install_response['actions']['LINK']]

    # Remove these packages from the actual target environment.
    remove_response = conda_api.remove(*packages_to_remove, name=environment)
    print(remove_response)
    # The below condition should always evaluate to True.
    # We can expect the above call to conda_api.remove() to throw
    # a CondaError error if something goes wrong.
    if remove_response['success']:
        print('\nThe following packages were successfully removed from {0}:\n\n{1}\n'
              .format(conda_api.get_prefix_envname(environment), '\n'.join(packages_to_remove)))

    # Cleanup - delete the temporary conda env.
    conda_api.remove_environment(temp_env)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print('USAGE: python remover.py ENVIRONMENT PACKAGE')
        sys.exit(1)

    environment = sys.argv[1]
    package = sys.argv[2]

    remove_package_with_dependencies(environment, package)
