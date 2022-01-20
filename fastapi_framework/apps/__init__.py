from .app import create_app

from .test_api import api_router
from .exceptions import exception_handlers
from .extensions import dependencies

app = create_app(
    routers=[api_router], 
    handlers=exception_handlers,
    dependencies=dependencies
)