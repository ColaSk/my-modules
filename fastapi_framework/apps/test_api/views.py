from typing import Any, Optional
from fastapi import APIRouter, Depends
from apps.extensions import success_response
from apps.extensions import RequestBase, RequestDependBase
from apps.exceptions.exception import UnicornException
from apps.extensions.route import MyRoute

router = APIRouter(route_class=MyRoute)

class TestRequest(RequestBase):
    name: str

@router.post('/test', status_code=201)
def test(body: TestRequest, request: dict = Depends(RequestDependBase)):
    return success_response(data=request)