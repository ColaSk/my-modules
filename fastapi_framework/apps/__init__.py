from .application import create_app

from .test_api import api_router
from .exceptions import exception_handlers
from .extensions import dependencies
from .middlewares import app_middleware

app = create_app(
    routers=[api_router], 
    handlers=exception_handlers,
    dependencies=dependencies,
    middlewares=app_middleware
)