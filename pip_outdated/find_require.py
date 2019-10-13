"""
Find requirements.
https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
"""

import pathlib
import re
from itertools import chain

from pkg_resources import Requirement, RequirementParseError
from setuptools.config import read_configuration

from .verbose import verbose

def iter_files(patterns):
    """Yield path.Path(file) from multiple glob patterns."""
    for pattern in patterns:
        if pathlib.Path(pattern).is_file():
            yield pathlib.Path(pattern)
        else:
            for file in pathlib.Path(".").glob(pattern):
                yield file
                
def iter_lines(file):
    """Yield line from a file. Handle '#' comment and '\' continuation escape.
    """
    if verbose():
        print(f"Parse: {file}")
    pre_line = ""
    with file.open("r", encoding="utf-8") as f:
        for line in f:
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
    for line in iter_lines(file):
        require = parse_require(line)
        if require:
            yield require
            
def parse_cfg(file):
    conf = read_configuration(file, ignore_option_errors=True)
    requires = []
    
    try:
        requires.extend(conf["options"]["setup_requires"])
    except KeyError:
        pass
        
    try:
        requires.extend(conf["options"]["install_requires"])
    except KeyError:
        pass
        
    try:
        requires.extend(chain.from_iterable(conf["options"]["extras_require"].values()))
    except KeyError:
        pass
    
    for require in requires:
        require = parse_require(require)
        if require:
            yield require
            
def find_require(files):
    for file in iter_files(files):
        requires = parse_cfg(file) if file.suffix == ".cfg" else parse_requirements(file)
        for require in requires:
            yield require
    
def parse_require(text):
    # strip options
    match = re.match(r"(.*?)\s--?[a-z]", text)
    if match:
        text = match.group(1)
    try:
        return Requirement.parse(text)
    except RequirementParseError:
        pass
    