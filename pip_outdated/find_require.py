"""
Find requirements.
https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
"""

from collections.abc import Iterable
from configparser import ConfigParser
import pathlib
import re

from packaging.requirements import Requirement, InvalidRequirement
from .verbose import verbose

def iter_files(patterns):
    """Yield path.Path(file) from multiple glob patterns."""
    for pattern in patterns:
        if pathlib.Path(pattern).is_file():
            yield pathlib.Path(pattern)
        else:
            yield from pathlib.Path(".").glob(pattern)
                
def file_to_lines(file):
    """Yield line from a file. Handle '#' comment and '\' continuation escape.
    """
    if verbose():
        print(f"Parse: {file}")
    with file.open("r", encoding="utf-8") as f:
        yield from parse_lines(f)

def parse_lines(lines: Iterable[str]):
    pre_line = ""
    for line in lines:
        match = re.match(r"(.*?)(^|\s)#", line)
        if match:
            yield pre_line + match.group(1)
            pre_line = ""
            continue
        if line.endswith("\\\n"):
            pre_line += line[0:-2]
            continue
        if line.endswith("\n"):
            yield pre_line + line[0:-1]
            pre_line = ""
            continue
        yield pre_line + line
        pre_line = ""

def parse_requirements(file):
    for line in file_to_lines(file):
        require = parse_require(line)
        if require:
            yield require

def parse_requirements_text(text: str):
    for line in parse_lines(text.splitlines(True)):
        require = parse_require(line)
        if require:
            yield require

def parse_cfg(file):
    conf = ConfigParser()
    conf.read(file, encoding="utf-8")

    def get_texts():
        try:
            yield conf["options"]["setup_requires"]
        except KeyError:
            pass
        try:
            yield conf["options"]["install_requires"]
        except KeyError:
            pass
        try:
            for key in conf["options.extras_require"]:
                yield conf["options.extras_require"][key]
        except KeyError:
            pass

    for text in get_texts():
        if not text:
            continue
        yield from parse_requirements_text(text)
    
def find_require(files):
    for file in iter_files(files):
        requires = parse_cfg(file) if file.suffix == ".cfg" else parse_requirements(file)
        yield from requires
    
def parse_require(text):
    # strip options
    match = re.match(r"(.*?)\s--?[a-z]", text)
    if match:
        text = match.group(1)
    try:
        return Requirement(text)
    except InvalidRequirement:
        return None
    
