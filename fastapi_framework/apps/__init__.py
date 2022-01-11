from .app import create_app

from .test_api import api_router

app = create_app(routers=[api_router])