# celery -A celery_app beat  --detach  --schedule ./celerybeat/celerybeat-schedule --logfile ./logs/celerybeat.log
celery -A celery_app  worker -l INFO