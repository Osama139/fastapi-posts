from fastapi import FastAPI
from . import models, database
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)
origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, tags=["users"])
app.include_router(post.router, tags=["posts"])
app.include_router(auth.router, tags=["authentication"])
app.include_router(vote.router, tags=["vote"])

@app.get("/")
def root():
    return {"message": "Hello World!"}