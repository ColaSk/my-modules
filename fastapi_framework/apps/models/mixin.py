from apps.exceptions import NotFound
from tortoise.models import Model
from tortoise import fields
from typing import Union

MODEL_TIME_FORMART = '%Y-%m-%d %H:%M:%S'


class ModelBase(Model):

    id = fields.IntField(pk=True, description='主键') # 32bit
    created = fields.DatetimeField(auto_now_add=True, null=False, description='创建时间')
    updated = fields.DatetimeField(auto_now=True, null=False, description='更新时间')
    is_del = fields.BooleanField(null=False, default=False, description='逻辑删除')

    @property
    def created_time(self):
        return self.created.strftime(MODEL_TIME_FORMART) if self.created else ''

    @property
    def updated_time(self):
        return self.updated.strftime(MODEL_TIME_FORMART) if self.updated else ''

    class Meta:
        abstract = True


class ModelMixin(object): 

    def to_dict(self, selects: tuple = None, excludes: tuple = None):
        
        if not hasattr(self, '_meta'):
            raise AssertionError('<%r> does not have attribute for _meta' % self)

        if selects:
            return {i: getattr(self, i) for i in selects}
        elif excludes:
            return {i: getattr(self, i) for i in self._meta.fields if i not in excludes}
        else:
            return {i: getattr(self, i) for i in self._meta.fields}

class ModelObject(object):

    def __init__(self, model: Model, pk: int):
        """_summary_

        Args:
            model (Model): 模型
            pk (int): 主键
        """        

        self._model = model
        self._pk = pk

    async def object(self, is_del: Union[bool, None]):
        
        if is_del == None:
            obj = await self._model.get_or_none(id=self._pk)
        else:
            obj = await self._model.get_or_none(id=self._pk, is_del=is_del)
        
        if not obj:
            raise NotFound(msg=f'{self._model} not found pk: {self._pk}, is_del: {is_del} object')
        
        return obj
        