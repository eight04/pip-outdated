import sys
import colorama
from termcolor import colored
from terminaltables import AsciiTable as Table

def make_row(outdate):
    if not outdate.outdated():
        return None
        
    def colored_current():
        if outdate.install_not_found() or outdate.install_not_wanted():
            return colored(str(outdate.version), "red", attrs=["bold"])
        return str(outdate.version)
        
    def colored_wanted():
        if outdate.pypi_not_found() or not outdate.wanted:
            return colored("None", "red", attrs=["bold"])
        if not outdate.install_not_found() and outdate.version < outdate.wanted:
            return colored(str(outdate.wanted), "green", attrs=["bold"])
        return str(outdate.wanted)
        
    def colored_latest():
        if outdate.pypi_not_found():
            return colored("None", "red", attrs=["bold"])
        if not outdate.install_not_found() and outdate.version < outdate.latest:
            return colored(str(outdate.latest), "green", attrs=["bold"])
        return str(outdate.latest)
    
    return [
        outdate.name,
        colored_current(),
        colored_wanted(),
        colored_latest()
    ]

def print_outdated(outdates, quiet: bool):
    colorama.init()
    
    data = [["Name", "Installed", "Wanted", "Latest"]]
    count = 0
    for count, outdate in enumerate(outdates, 1):
        row = make_row(outdate)
        if row:
            data.append(row)
            
    if not count:
        print(colored("No requirements found.", "red"))
        return
        
    if len(data) == 1:
        print(colored("Everything is up-to-date!", "cyan", attrs=["bold"]))
        return
        
    print(colored("Red = unavailable/outdated/out of version specifier", "red", attrs=["bold"]))
    print(colored("Green = updatable", "green", attrs=["bold"]))
    table = Table(data)
    print(table.table)
    if not quiet:
        sys.exit(1)
    