from tortoise.models import Model
from tortoise import fields


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


class ModelMixin(object): ...