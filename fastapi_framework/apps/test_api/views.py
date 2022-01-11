from fastapi import APIRouter

router = APIRouter()

@router.get('/test')
def test():
    return "hello word"