import time

from abc import ABCMeta, abstractmethod


class Article:
    def __init__(self, slug, title, description, body, author_id):
        now = time.time()
        self._slug = slug
        self._title = title
        self._description = description
        self._body = body
        self._author_id = author_id
        self._created_at = now
        self._updated_at = now

    @property
    def slug(self):
        return self._slug

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def body(self):
        return self._body

    @property
    def author_id(self):
        return self._author_id

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        self._updated_at = updated_at


class ArticleRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, article: Article) -> Article:
        pass
