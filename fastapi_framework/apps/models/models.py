from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext
from .mixin import ModelBase, ModelMixin

class User(ModelBase, ModelMixin):

    name = fields.CharField(max_length=255, null=False, unique=True, description='名称')
    hash_pwd = fields.CharField(max_length=255, null=False, description='密码hash')

    class Meta:
        table = 'users'
        table_description = '用户表'

    @property
    def pwdcontext(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def password(self):
        return self.hash_pwd

    @password.setter
    def password(self, value):
        self.hash_pwd = self.pwdcontext.hash(value)

    def check_password(self, password: str) -> bool:
        return self.pwdcontext.verify(password, self.password)