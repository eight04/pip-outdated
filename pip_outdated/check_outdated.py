from packaging.utils import canonicalize_name
from packaging.version import parse as parse_version
from pkg_resources import get_distribution, DistributionNotFound
import requests

from .verbose import verbose

class OutdateResult:
    def __init__(self, requirement, version, all_versions):
        self.requirement = requirement
        self.name = requirement.name
        self.version = version
        self.wanted = None
        self.latest = None
        
        if all_versions:
            try:
                self.wanted = next(v for v in reversed(all_versions)
                                   if v in requirement.specifier)
            except StopIteration:
                pass
            self.latest = all_versions[-1]
        
    def install_not_found(self):
        return self.version is None
        
    def install_not_wanted(self):
        return self.version not in self.requirement.specifier
        
    def pypi_not_found(self):
        return self.latest is None
        
    def outdated(self):
        return self.version != self.wanted or self.version != self.latest

def get_current_version(name):
    try:
        return parse_version(get_distribution(name).version)
    except DistributionNotFound:
        pass
        
def get_pypi_versions(name, session=requests):
    r = session.get(f"https://pypi.org/pypi/{name}/json")
    if r.status_code != 200:
        return None
    keys = [parse_version(v) for v in r.json()["releases"].keys()]
    keys.sort()
    return keys

def check_outdated(requires):
    s = requests.Session()
    for require in requires:
        if verbose():
            print(f"Checking: {require.name} {require.specifier}")
        name = canonicalize_name(require.name)
        current_version = get_current_version(name)
        pypi_versions = get_pypi_versions(name, s)
        yield OutdateResult(require, current_version, pypi_versions)
