__version__ = "0.0.0"

def pip_outdated(files=None):
    from .find_require import find_require
    from .check_outdated import check_outdated
    from .print_outdated import print_outdated
    requires = find_require(files)
    outdated_results = check_outdated(requires)
    print_outdated(outdated_results)
    
def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        prog="pip-outdated",
        description="Find outdated dependencies in your requirements.txt or "
                    "setup.cfg file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "file", nargs="*", default=["requirements.txt"], metavar="<file>",
        help="Read dependencies from requirement files. This option accepts "
             "glob pattern.")
    return parser.parse_args()

def main():
    args = parse_args()
    pip_outdated(files=args.file)
    