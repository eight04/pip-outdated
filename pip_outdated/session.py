import aiohttp


def get_session() -> aiohttp.ClientSession:
    headers = {"User-Agent": "pip-outdated"}
    connector = aiohttp.TCPConnector(limit=5)
    return aiohttp.ClientSession(headers=headers, connector=connector)    
