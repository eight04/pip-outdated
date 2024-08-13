import pytest
from pip_outdated.check_outdated import get_pypi_versions
from pip_outdated.session import get_session

@pytest.mark.asyncio
async def test_pytz():
    async with get_session() as session:
        await get_pypi_versions("pytz", session)
    
