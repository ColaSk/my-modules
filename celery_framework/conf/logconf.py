import os
from .setting import LogConfig


LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LogConfig.LOG_DIR, "celery-main.log"),
            'when': 'midnight',
            'backupCount': 10,
            'encoding': 'utf-8'
        }
    },
    'root': {
        'handlers': ['console', 'default'],
        'level': 'INFO'
    }
}
