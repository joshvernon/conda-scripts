#!/usr/bin/env python
#
# updater.py
#
# Updates all packages in all installed conda environments.
# This script should be run under the root conda environment.

import os.path

import conda_api

from utils import get_root_prefix

def update_all(update_root=True, *blacklist_envs):
    """Updates all conda packages in all installed conda environments.

    Required arguments:
    update_root -- A Boolean flag that specifies whether the root conda
                   environment should be updated (default True).

    Optional arguments:
    *blacklist_envs -- Names of environments you don't want updated.

    Example usage:
    update_all(True, 'special_env1', 'special_env2')
    This will update all conda environments (including root) but excluding
    special_env1 and special_env2.
    """
    # Before we do anything, set the ROOT_PREFIX
    # variable so conda_api knows where to work from.
    conda_api.set_root_prefix(get_root_prefix())

    # Get all active environments, excluding the ones in the blacklist.
    envs = [
        os.path.basename(env) for env in conda_api.get_envs()
        if os.path.basename(env) not in blacklist_envs
    ]

    print('ROOT_PREFIX is set to: {0}'.format(conda_api.ROOT_PREFIX))

    if update_root:
        root_update_result = conda_api.update(use_local=True, all=True)
        print('Result from environment root:\n{0}'.format(root_update_result))

    for env_name in envs:
        # Update all packages in the environment.
        env_update_result = conda_api.update(env=env_name, all=True)
        print('Result from environment {0}:\n{1}'.format(env_name, env_update_result))

def pip_update(**pip_package_specs):
    """Updates pip packages in their respective conda environments.

    Keyword arguments:
    **pip_package_specs -- The key is the name of the environment, and the
                           value is an iterable of the pip package names
                           in that environment you want to update.

    Example usage:
    pip_package_specs = {'conda_env1':('autobahn','six','txaio',),
                         'conda_env2':('pika',)}
    pip_update(**pip_package_specs)
    This will update autobahn, six, and txaio in the conda environment
    'conda_env1', and pika in the environment 'conda_env2'.
    """
    if pip_package_specs:
        conda_api.set_root_prefix(get_root_prefix())
        for env, packages in pip_package_specs.items():
            pip_args = ['install', '-q', '-U']
            pip_args.extend(packages)
            # Equivalent of running 'pip install -q -U package1 package2 ...',
            # but runs it inside the appropriate conda environment.
            p = conda_api.process(name=env, cmd='pip', args=pip_args)
            p.communicate()
            print('Updated the following pip packages in environment {0}: {1}'\
                  .format(env, ' '.join(packages)))

if __name__ == '__main__':
    update_all()
        
