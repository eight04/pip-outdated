"""
Find requirements.
https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
"""

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
    lines = iter_lines(file)
    
    # find install_requires
    for line in lines:
        match = re.match(r"install_requires\s*=\s*(.*)", line)
        if not match:
            continue
        require = parse_require(match.group(1))
        if require:
            yield require
        break
            
    # find requirements
    for line in lines:
        if re.match(r"\s*$", line):
            # ignore empty line
            continue
        # must starts with whitespace (indented)
        match = re.match(r"\s+(.+)", line)
        if not match:
            break
        require = parse_require(match.group(1))
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
        return Requirement(text)
    except InvalidRequirement:
        pass
    