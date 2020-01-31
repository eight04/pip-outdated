"""Simple namespace to share verbose state."""

VERBOSE: bool = None

def set_verbose(value: bool) -> None:
    global VERBOSE
    VERBOSE = value
    
def verbose() -> bool:
    return VERBOSE
