"""moopaste main script entrypoint
"""

from __future__ import print_function

import argparse
import logging
import sys

from moopaste import __version__
from moopaste.capture.clipboard import clipboard_file, paste_file
from moopaste.config import write_config, resolve_config, config_option
from moopaste.config import update_parser_arguments


VERBOSITY = {
    2: logging.DEBUG,
    1: logging.INFO,
    0: logging.WARNING,
    -1: logging.ERROR,
    -2: logging.CRITICAL,
}


def create_parser():
    """Creates the default argument parser.

    Returns
    -------
    parser : ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--config-file')
    parser.add_argument('--update-config', action='store_true')
    update_parser_arguments(parser)
    parser.add_argument('command', default='paste', nargs='?',
                        choices=('init', 'paste', 'clipboard', 'screenshot'))
    return parser


@config_option('-v', '--verbose', action='count', default=0)
@config_option('-q', '--quiet', action='count', default=0)
def config_logging(args):
    """Sets up logging from the command line arguments and config.
    """
    logging.basicConfig()
    logger = logging.getLogger('moopaste')
    logger.setLevel(VERBOSITY[args.verbose-args.quiet])


def main():
    """moopaste sharing utility
    """
    parser = create_parser()
    args = parser.parse_known_args()
    if args.command == 'init':
        config = resolve_config()
    else:
        config = resolve_config(args.config_file)
    parser.set_defaults(config)
    args = parser.parse_args()
    config_logging(args)
    if args.command == 'init' or args.update_config:
        write_config(config, args.config_file)
    if args.command == 'init':
        return 0
    localfile = None
    if args.command == 'paste':
        localfile = paste_file()
    elif args.command == 'clipboard':
        localfile = clipboard_file()
    return 0


if __name__ == '__main__':
    sys.exit(main())
