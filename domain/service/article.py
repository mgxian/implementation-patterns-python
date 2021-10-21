from abc import ABCMeta, abstractmethod

from domain.model.article import Article, ArticleRepository


class Clock(metaclass=ABCMeta):
    @abstractmethod
    def now(self) -> float:
        pass


class ArticleService:
    def __init__(self, article_repository: ArticleRepository, clock):
        self._article_repository = article_repository
        self._clock = clock

    def create_article(self, title, description, body, author_id) -> Article:
        slug = title.lower().replace(' ', '-')
        if self._article_repository.exists_by_slug(slug):
            raise ArticleExistedException("the article with slug {} already exists".format(slug))
        article = Article(slug, title, description, body, author_id)
        now = self._clock.now()
        article.created_at = now
        article.updated_at = now
        return self._article_repository.save(article)


class ArticleExistedException(Exception):
    def __init__(self, message):
        super().__init__(message)
