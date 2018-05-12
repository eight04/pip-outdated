"""Simple namespace to share verbose state."""

VERBOSE = None

def set_verbose(value):
    global VERBOSE
    VERBOSE = value
    
def verbose():
    return VERBOSE
