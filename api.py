from fastapi import FastAPI, APIRouter
from chunk import split_router


app = FastAPI()

router = APIRouter()


app.include_router(split_router, prefix='/split')
