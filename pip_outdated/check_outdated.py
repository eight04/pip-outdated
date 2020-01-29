from packaging.utils import canonicalize_name
from packaging.version import parse as parse_version
from pkg_resources import get_distribution, DistributionNotFound

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
        
async def get_pypi_versions(name, session):
    async with session.get(f"https://pypi.org/pypi/{name}/json") as r:
        if r.status != 200:
            return None
        keys = [parse_version(v) for v in (await r.json())["releases"].keys()]
        keys = [v for v in keys if not v.is_prerelease]
        keys.sort()
        return keys
    
async def get_outdate_result(require, session):
    if verbose():
        print(f"Checking: {require.name} {require.specifier}")
    name = canonicalize_name(require.name)
    current_version = get_current_version(name)
    pypi_versions = await get_pypi_versions(name, session)
    return OutdateResult(require, current_version, pypi_versions)
