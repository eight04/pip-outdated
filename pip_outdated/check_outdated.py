from dataclasses import dataclass
from typing import List, Optional

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version
from packaging.version import parse as parse_version
from pkg_resources import DistributionNotFound, get_distribution

from .verbose import verbose


@dataclass
class OutdateResult:
    requirement: Requirement
    version: Optional[Version]
    all_versions: List[Version]

    wanted: Optional[Version] = None
    latest: Optional[Version] = None

    def __post_init__(self):
        if self.all_versions:
            try:
                self.wanted = next(v for v in reversed(self.all_versions)
                                   if v in self.requirement.specifier)
            except StopIteration:
                pass
            self.latest = self.all_versions[-1]

    @property
    def name(self) -> str:
        return self.requirement.name

    def install_not_found(self) -> bool:
        return self.version is None
        
    def install_not_wanted(self) -> bool:
        return self.version not in self.requirement.specifier
        
    def pypi_not_found(self) -> bool:
        return self.latest is None
        
    def outdated(self) -> bool:
        return self.version != self.wanted or self.version != self.latest

def get_current_version(name: str) -> Optional[Version]:
    try:
        return parse_version(get_distribution(name).version)
    except DistributionNotFound:
        pass
        
async def get_pypi_versions(name: str, session) -> List[Version]:
    async with session.get(f"https://pypi.org/pypi/{name}/json") as r:
        if r.status != 200:
            return None
        keys = [parse_version(v) for v in (await r.json())["releases"].keys()]
        keys = [v for v in keys if not v.is_prerelease]
        keys.sort()
        return keys
    
async def check_outdated(require, session) -> OutdateResult:
    if verbose():
        print(f"Checking: {require.name} {require.specifier}")
    name = canonicalize_name(require.name)
    current_version = get_current_version(name)
    pypi_versions = await get_pypi_versions(name, session)
    return OutdateResult(require, current_version, pypi_versions)
