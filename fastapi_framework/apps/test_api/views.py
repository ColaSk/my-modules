from fastapi import APIRouter
from apps.extensions import success_response
from apps.extensions import RequestBase
from apps.exceptions.exception import UnicornException

router = APIRouter()

class TestRequest(RequestBase):
    name: str

@router.post('/test', status_code=201)
def test(request: TestRequest):
    return success_response(data=request)