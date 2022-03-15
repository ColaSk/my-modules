from .application import create_app

from .test_api import api_router
from .admin import api_router as admin_router
from .exceptions import exception_handlers
from .extensions import dependencies
from .middlewares import app_middleware
from config import ORM_LINK_CONF, setting


app = create_app(
    config=setting.app.dict(),
    routers=(api_router, admin_router), 
    handlers=exception_handlers,
    dependencies=dependencies,
    middlewares=app_middleware,
    db_config=ORM_LINK_CONF
)