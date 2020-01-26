import asyncio
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

from pkg_resources import DistributionNotFound, get_distribution

import aiohttp
from asgiref.sync import async_to_sync
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version
from packaging.version import parse as parse_version

from .verbose import verbose


@dataclass
class OutdateResult:
    requirement: Requirement
    version: Version
    all_versions: List[Version]

    def name(self) -> str:
        return self.requirement.name

    def wanted(self) -> Version:
        try:
            return next(v for v in reversed(self.all_versions) if v in self.requirement.specifier)
        except StopIteration:
            pass
        return None

    def latest(self) -> Version:
        return self.all_versions[-1] if self.all_versions else None

    def install_not_found(self) -> bool:
        return self.version is None

    def install_not_wanted(self) -> bool:
        return self.version not in self.requirement.specifier

    def pypi_not_found(self) -> bool:
        return self.latest() is None

    def outdated(self) -> bool:
        return self.version != self.wanted() or self.version != self.latest()


def get_current_version(name: str) -> Optional[Version]:
    try:
        return parse_version(get_distribution(name).version)
    except DistributionNotFound:
        pass


async def get_pypi_versions(session, package_name: str) -> Tuple[str, List[Version]]:
    ''' For a given package, fetch the versions available on pypi '''
    async with session.get(f"https://pypi.org/pypi/{package_name}/json") as response:
        if verbose():
            print(f'Checking available versions of {package_name}')
        if response.status != 200:
            return (package_name, [])
        json_response = await response.json()
        keys = (parse_version(v) for v in json_response["releases"].keys())
        keys = (v for v in keys if not v.is_prerelease)
        return (package_name, sorted(keys))


def check_outdated(requires: Iterable[Requirement]):
    installed_requirements = list(requires)

    # Fetch from pypi in parallel: mapping from name to list of versions
    canonical_names = [canonicalize_name(r.name) for r in installed_requirements]
    pypi_versions_by_canonical_name = fetch_pypi_versions(canonical_names)

    for require, can_name in zip(installed_requirements, canonical_names):
        yield OutdateResult(
            require,
            get_current_version(can_name),
            pypi_versions_by_canonical_name[can_name]
        )


@async_to_sync
async def fetch_pypi_versions(canonical_package_names: List[str]) -> Dict[str, List[Version]]:
    ''' Construct a mapping with for each of the requested packages,
        the list of available pypi versions
    '''
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=10, ttl_dns_cache=None)
        ) as session:
            return {
                r[0]: r[1]
                for r in
                await asyncio.gather(*(get_pypi_versions(session, t) for t in canonical_package_names))
            }
