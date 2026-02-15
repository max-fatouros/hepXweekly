"""
# hep-ex-weekly
"""
import mjaf

import argparse

from rich_argparse import RawDescriptionRichHelpFormatter, ArgumentDefaultsRichHelpFormatter

from hep_ex_weekly._utils.constants import VERSION

import logging

import rich
import rich.markdown

# get this module's logger
log = logging.getLogger(__name__)


def parse_args():
    class CustomFormatter(
        RawDescriptionRichHelpFormatter,
        ArgumentDefaultsRichHelpFormatter
    ):
        """This just combines the two formatters using multiple inheritance."""
        pass

    parser = argparse.ArgumentParser(
        description=rich.markdown.Markdown(__doc__, style="argparse.text"),
        formatter_class=CustomFormatter,
    )
    

    parser.add_argument(
        '--log-level',
        action='store',
        choices=[
            'debug',
            'info',
            'warning',
            'error',
            'critical',
        ],
        default='warning'
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"[argparse.prog]%(prog)s[/] version [i]{VERSION}[/]"
    )

    args = parser.parse_args()
    
    return args

    
def main():
    args = parse_args()
    # Configure module-root logger
    mjaf.logging.set_handlers(
        logger_name="hep_ex_weekly",
        level=args.log_level.uppter()
    )

    # get this module's logger
    log = logging.getLogger(__name__)


if __name__ == '__main__':
    main()
