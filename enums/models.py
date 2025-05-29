from enum import Enum


class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class Location(str, Enum):
    MSK = "MSK"
    SPB = "SPB"