from datetime import datetime

DEFAULT_TIME_FORMAT = '%Y:%m:%d %H:%M:%S'

def get_curr_time(format: str = DEFAULT_TIME_FORMAT):
    return datetime.now().strftime(format)