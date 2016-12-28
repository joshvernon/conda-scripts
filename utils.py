import os.path

def get_root_prefix():
    """Gets the root prefix for a user's conda installation."""
    return os.path.expanduser('~/miniconda')
