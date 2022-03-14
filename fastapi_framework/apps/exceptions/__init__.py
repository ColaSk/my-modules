from .exception import base_exception_handler, exception_handler
from .exception import UnicornException, NotFound


exception_handlers = {
    UnicornException : base_exception_handler,
    Exception: exception_handler,
    NotFound: base_exception_handler
}