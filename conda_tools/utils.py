from os.path import exists, expanduser

def get_root_prefix():
    """Gets the root prefix for a user's conda installation."""
    if exists(expanduser('~/miniconda')):
        root_prefix = expanduser('~/miniconda')
    elif exists(expanduser('~/miniconda2')):
        root_prefix = expanduser('~/miniconda2')
    else:
        root_prefix = None
    return root_prefix
