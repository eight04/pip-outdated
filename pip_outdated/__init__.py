import argparse

__version__ = "0.2.0"

def parse_args():
    parser = argparse.ArgumentParser(
        prog="pip-outdated",
        description="Find outdated dependencies in your requirements.txt or "
                    "setup.cfg file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print verbose information.")
    parser.add_argument(
        "file", nargs="*", default=["requirements.txt", "setup.cfg"], metavar="<file>",
        help="Read dependencies from requirements files. This option accepts "
             "glob pattern.")
    return parser.parse_args()

def main():
    args = parse_args()
    
    from .verbose import set_verbose
    set_verbose(args.verbose)
    
    from .find_require import find_require
    from .check_outdated import check_outdated
    from .print_outdated import print_outdated
    requires = find_require(args.file)
    outdated_results = check_outdated(requires)
    print_outdated(outdated_results)
    