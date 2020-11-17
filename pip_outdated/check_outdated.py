from dataclasses import dataclass
from typing import List, Optional, TypedDict

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version
from packaging.version import parse as parse_version
from pkg_resources import DistributionNotFound, get_distribution

from .verbose import verbose

class Release(TypedDict):
    version: Version
    date: str

@dataclass
class OutdateResult:
    requirement: Requirement
    version: Optional[Version]
    all_releases: List[Release]

    wanted_version: Optional[Version] = None
    wanted_date: Optional[str] = None
    latest_version: Optional[Version] = None
    latest_date: Optional[str] = None

    def __post_init__(self):
        if self.all_releases:
            try:
                wanted = next(r for r in reversed(self.all_releases)
                              if r['version'] in self.requirement.specifier)
                self.wanted_version = wanted['version']
                self.wanted_date = wanted['date']
            except StopIteration:
                pass
            latest = self.all_releases[-1]
            self.latest_version = latest['version']
            self.latest_date = latest['date']

    @property
    def name(self) -> str:
        return self.requirement.name

    def install_not_found(self) -> bool:
        return self.version is None

    def install_not_wanted(self) -> bool:
        return self.version not in self.requirement.specifier

    def pypi_not_found(self) -> bool:
        return self.latest_version is None

    def outdated(self) -> bool:
        return (
            self.version != self.wanted_version or
            self.version != self.latest_version
        )

def get_current_version(name: str) -> Optional[Version]:
    try:
        return parse_version(get_distribution(name).version)
    except DistributionNotFound:
        pass

async def get_pypi_releases(name: str, session) -> List[Version]:
    async with session.get(f"https://pypi.org/pypi/{name}/json") as r:
        if r.status != 200:
            return None
        releases = []
        for v, info in (await r.json())["releases"].items():
            version = parse_version(v)
            if version.is_prerelease or len(info) == 0:
                continue
            releases.append({
                'version': version,
                'date': info[0]['upload_time'][:10]
            })
        releases.sort(key=lambda release: release.get("version"))
        return releases

async def check_outdated(require, session) -> OutdateResult:
    if verbose():
        print(f"Checking: {require.name} {require.specifier}")
    name = canonicalize_name(require.name)
    current_version = get_current_version(name)
    pypi_releases = await get_pypi_releases(name, session)
    return OutdateResult(require, current_version, pypi_releases)
