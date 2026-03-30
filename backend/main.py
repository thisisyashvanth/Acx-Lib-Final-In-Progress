from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import Base, engine

from api.user_api import router as user_router
from api.auth_api import router as auth_router
from api.book_api import router as book_router
from api.request_api import router as request_router

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Acxhange Library System", lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(book_router)
app.include_router(request_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)