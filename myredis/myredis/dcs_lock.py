import datetime
from contextlib import ContextDecorator
from typing import Any, Union
from .client import RedisBase

class DistributedLock(RedisBase):

    """双重分布式锁"""

    _key = "dcs_lock"
    _timeout = 3600 # s

    @property
    def key(self):
        return f'{self._prefix_key}:{self._key}'
    
    def get(self, key):
        velue = self.client.get(key)
        return velue

    def setnx(self, key, velue):
        return self.client.setnx(key, velue)
    
    def getset(self, key, velue):
        old_velue = self.client.getset(key, velue)
        return old_velue
    
    def expire(self, key, seconds):
        return self.client.expire(key, seconds)
    
    def delete(self, *key):
        return self.client.delete(*key)

    def create_lock(self):
        """创建锁
        key:value
        key:时间戳+超时时间
        """
        curr_time = datetime.now().timestamp()
        end_time = curr_time + self._timeout

        # 获取锁
        lock = self.setnx(self.key, end_time)

        # 获取到锁, 设置超时时间
        if lock:
            self.expire(self.key, self._timeout)
            return str(end_time)

        # 获取旧锁
        oldlock = self.get(self.key)

        # 当前申请锁的时间大于旧的锁
        if oldlock and curr_time > float(oldlock):

            _oldlock = self.getset(self.key, end_time)
            if not _oldlock or oldlock == _oldlock:
                return str(end_time)

            return

        return

    def delete_lock(self):
        """删除锁"""
        return self.delete(self.key)

    def verify_lock(self, verify):
        """验证锁"""
        return bool(self.get(self.key) == verify)


class DistributedLockContext(ContextDecorator):

    def __init__(self, lock_cls: DistributedLock = DistributedLock, *args, **kwargs):
        self._lock_object = lock_cls(*args, **kwargs)

    @property
    def lock_object(self):
         return self._lock_object

    def __enter__(self):
        self.lock = self.lock_object.create_lock()
        if not self.lock:
            raise Exception(f'Lock not acquired')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.lock_object.verify_lock(self.lock):
            self.lock_object.delete_lock()