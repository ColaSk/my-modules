from pydantic import BaseModel, Field
from utils import get_curr_time

class RequestBase(BaseModel):
    reqtime: str = Field(get_curr_time(), description='request time') # TODO: 动态时间

