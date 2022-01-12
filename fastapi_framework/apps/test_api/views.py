from typing import Any, Optional
from fastapi import APIRouter, Depends, Cookie
from apps.extensions import success_response
from apps.extensions import RequestBase, request_base, RequestDependBase
from apps.exceptions.exception import UnicornException

router = APIRouter()

class TestRequest(RequestBase):
    name: str

@router.post('/test', status_code=201)
def test(body: TestRequest, request: dict = Depends(RequestDependBase)):
    return success_response(data=request)