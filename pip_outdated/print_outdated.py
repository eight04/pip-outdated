import sys
from typing import Awaitable, List, Optional

import colorama

from termcolor import colored
from terminaltables import AsciiTable as Table

from .check_outdated import OutdateResult


def make_row(outdate: OutdateResult, dates: bool) -> Optional[List[str]]:
    if not outdate.outdated():
        return None

    def colored_current():
        if outdate.install_not_found() or outdate.install_not_wanted():
            return colored(str(outdate.version), "red", attrs=["bold"])
        return str(outdate.version)

    def colored_wanted_version():
        if outdate.pypi_not_found() or not outdate.wanted_version:
            return colored("None", "red", attrs=["bold"])
        if not outdate.install_not_found() and outdate.version < outdate.wanted_version:
            return colored(str(outdate.wanted_version), "green", attrs=["bold"])
        return str(outdate.wanted_version)

    def colored_latest_version():
        if outdate.pypi_not_found():
            return colored("None", "red", attrs=["bold"])
        if not outdate.install_not_found() and outdate.version < outdate.latest_version:
            return colored(str(outdate.latest_version), "green", attrs=["bold"])
        return str(outdate.latest_version)

    if dates:
        row = [
            outdate.name,
            colored_current(),
            colored_wanted_version(),
            outdate.wanted_date,
            colored_latest_version(),
            outdate.latest_date
        ]
    else:
        row = [
            outdate.name,
            colored_current(),
            colored_wanted_version(),
            colored_latest_version()
        ]
    return row

async def print_outdated(
        outdates: List[Awaitable[OutdateResult]],
        quiet: bool,
        dates: bool
    ):
    colorama.init()
    if dates:
        data = [["Name", "Installed", "Wanted", "", "Latest", ""]]
    else:
        data = [["Name", "Installed", "Wanted", "Latest"]]
    count = 0
    for count, outdate in enumerate(outdates, 1):
        row = make_row(await outdate, dates)
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
