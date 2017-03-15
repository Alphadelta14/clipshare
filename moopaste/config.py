"""Config resolution and initialization
"""
import json
import os
import warnings

CONFIG_DEFAULTS = {}
PARSER_ARGS = []

DEFAULT_USER_CONFIG_PATH = '~/.moopaste/config.json'
DEFAULT_PATHS = (
    DEFAULT_USER_CONFIG_PATH,
)


def config_option(*name_or_flags, **kwargs):
    if 'default' not in kwargs:
        raise ValueError('A default is expected for this wrapper')
    dest = None
    for name in name_or_flags:
        if not name.startswith('-'):
            raise ValueError('{}: Only --optional arguments permitted'.format(name))
        if len(name.strip('-')) == 1:
            continue
        dest = name.strip('-').replace('-', '_')
    dest = kwargs.get('dest') or dest
    if not dest:
        raise ValueError('No argument target found: *{}'.format(name_or_flags))
    CONFIG_DEFAULTS[dest] = kwargs['default']
    PARSER_ARGS.append((name_or_flags, kwargs))

    def wrapper(func):
        return func
    return wrapper


def update_parser_arguments(parser):
    for args, kwargs in PARSER_ARGS:
        parser.add_argument(*args, **kwargs)


def resolve_config(*extra_paths, **extra_values):
    r"""Resolves entire configuration.

    Default configuration is considered, then user config files, provided
    config files, then finally passed config arguments.

    Parameters
    ----------
    extra_paths : \*str
        Additional paths to consider.
    extra_values : \*\*dict
        Additional sections to use.

    Returns
    -------
    config : dict
    """
    config = CONFIG_DEFAULTS.copy()

    def config_update(overrides, name):
        for key in overrides:
            if key not in config:
                warnings.warn('{}: {} is not a known config key.'.format(name, key))
            config[key] = overrides[key]

    for path in DEFAULT_PATHS+extra_paths:
        if path is None:
            continue
        resolved_path = os.path.expanduser(path)
        if not os.path.exists(resolved_path):
            continue
        with open(resolved_path) as handle:
            path_config = json.load(handle)
            config_update(path_config, path)
        config_update(extra_values, 'command-supplied')
    return config


def write_config(config, path=None):
    """Creates a user-configuration file from parsed config.

    Parameters
    ----------
    config : dict
    path : str, optional
        Location to be specied. If not, it uses `DEFAULT_USER_CONFIG_PATH`
    """
    if path is None:
        path = DEFAULT_USER_CONFIG_PATH
    resolved_path = os.path.expanduser(path)
    with open(resolved_path, 'w') as handle:
        json.dump(config, handle, sort_keys=True, indent=2)
