from fastapi import APIRouter, status
from pydantic import BaseModel

from domain.impl.db.article_repository import ArticleRepositoryDB
from domain.service.article import ArticleService
from provider.system_clock import SystemClock

router = APIRouter()

article_repository = ArticleRepositoryDB()
system_clock = SystemClock()
article_service = ArticleService(article_repository, system_clock)


class ArticleCreateRequest(BaseModel):
    title: str
    description: str
    body: str
    author_id: int


class ArticleResponse(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    author_id: int
    created_at: float
    updated_at: float


@router.post("/articles", status_code=status.HTTP_201_CREATED, response_model=ArticleResponse)
def create_article(request: ArticleCreateRequest):
    article = article_service.create_article(request.title, request.description, request.body, request.author_id)
    response = {
        "slug": article.slug,
        "title": article.title,
        "description": article.description,
        "body": article.body,
        "author_id": article.author_id,
        "created_at": article.created_at,
        "updated_at": article.updated_at
    }
    return response
