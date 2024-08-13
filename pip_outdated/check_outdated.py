import asyncio
from dataclasses import dataclass
from typing import List, Optional

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version, InvalidVersion
from packaging.version import parse as parse_version

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
        if self.version is None:
            return False
        return self.version not in self.requirement.specifier
        
    def pypi_not_found(self) -> bool:
        return self.latest is None
        
    def outdated(self) -> bool:
        return self.version != self.wanted or self.version != self.latest

async def get_local_version(name: str) -> Optional[Version]:
    p = await asyncio.create_subprocess_shell(
        f"pip show {name}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        )
    stdout, _ = await p.communicate()
    if p.returncode != 0:
        return None
    for line in stdout.decode().splitlines():
        if line.startswith("Version: "):
            return parse_version(line[9:])
        
async def get_pypi_versions(name: str, session) -> List[Version]:
    async with session.get(f"https://pypi.org/pypi/{name}/json") as r:
        r.raise_for_status()
        keys = []
        for s in (await r.json())["releases"].keys():
            try:
                version = parse_version(s)
            except InvalidVersion:
                continue
            if version.is_prerelease:
                continue
            keys.append(version)
        keys.sort()
        return keys
    
async def check_outdated(require, session) -> OutdateResult:
    if verbose():
        print(f"Checking: {require.name} {require.specifier}")
    name = canonicalize_name(require.name)
    current_version = await get_local_version(name)
    pypi_versions = await get_pypi_versions(name, session)
    return OutdateResult(require, current_version, pypi_versions)
