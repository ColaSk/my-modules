from celery import Celery
from conf.setting import CeleryConfig

def create_celery_app(config):
    app = Celery('tasks')
    app.config_from_object(config)
    
    return app


app = create_celery_app(CeleryConfig)