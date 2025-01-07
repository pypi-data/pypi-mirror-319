from enum import Enum

# CadQuery centering constants for common options - (width, depth, height)
center_w = (True, False, False)
center_d = (False, True, False)
center_h = (False, False, True)
center_wd = (True, True, False)
center_wh = (True, False, True)
center_dh = (False, True, True)


class LogLevel(Enum):
    TRACE = 0
    DEBUG = 10
    INFO = 20
    ERROR = 30
