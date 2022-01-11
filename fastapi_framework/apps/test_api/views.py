from fastapi import APIRouter
from pydantic import Field
from apps.extensions import success_response
from apps.extensions import RequestBase

router = APIRouter()

class TestRequest(RequestBase):
    name: str

@router.post('/test')
def test(request: TestRequest):
    return success_response(data=request)