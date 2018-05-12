"""
Find requirements.
https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
"""

import pathlib
import re
from packaging.requirements import Requirement, InvalidRequirement

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
    pre_line = ""
    with file.open("r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"(.+?)\s#", line)
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
            
def find_require(files):
    requires = []
    
    # in requirements file
    for file in iter_files(files):
        for line in iter_lines(file):
            requires.append(parse_require(line))
                
    # setup.cfg
    setup_file = iter_lines(pathlib.Path("setup.cfg"))
    for line in setup_file:
        match = re.match(r"install_requires\s*=\s*(.*)", line)
        if match:
            requires.append(parse_require(match.group(1)))
            break
            
    for line in setup_file:
        if re.match(r"\s*$", line):
            # empty line
            continue
        match = re.match(r"\s+(.+)", line)
        if not match:
            break
        requires.append(parse_require(match.group(1)))
        
    return [r for r in requires if r]
    
def parse_require(text):
    # strip options
    match = re.match(r"(.*?)\s--?[a-z]", text)
    if match:
        text = match.group(1)
    try:
        return Requirement(text)
    except InvalidRequirement:
        pass
    