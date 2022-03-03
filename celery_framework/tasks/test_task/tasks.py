import logging
from tasks.application import app

logger = logging.getLogger(__name__)

@app.task(name='add', bind=True)
def add(self, x, y):
    print(f'{self.request.id}')
    return x + y

@app.task(name='test_beat')
def test_beat():
    logger.info('test_beat')