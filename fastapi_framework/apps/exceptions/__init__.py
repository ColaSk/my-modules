from .exception import core_exception_handler
from .exception import UnicornException


exception_handlers = {
    UnicornException : core_exception_handler
}