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
    This will update all conda environments (including root) but exluding
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

if __name__ == '__main__':
    update_all()
        
