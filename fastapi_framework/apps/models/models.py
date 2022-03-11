from tortoise.models import Model
from tortoise import fields
from .mixin import ModelBase, ModelMixin

class User(ModelBase, ModelMixin):

    name = fields.CharField(max_length=255, null=False, description='名称')
    hash_pwd = fields.CharField(max_length=255, null=False, description='密码hash')