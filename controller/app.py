from fastapi import FastAPI
from controller import article

app = FastAPI()
app.include_router(article.router)
