import time
from grappa import expect
from controller.app import app
from fastapi.testclient import TestClient
from fastapi import status

from domain.model.article import Article
from domain.service.article import ArticleService, ArticleExistedException

client = TestClient(app)


class TestArticle:
    def setup(self):
        self.url = '/articles'

    def test_it_can_create_an_article(self, monkeypatch):
        article = {'title': 'Fake Article', 'description': 'Description', 'body': 'Something', 'author_id': 1}
        now = time.time()

        def mock_create_article(*args, **kwargs):
            result = Article("fake-article", "Fake Article", "Description", "Something", 1)
            result.created_at = now
            result.updated_at = now
            return result

        monkeypatch.setattr(ArticleService, "create_article", mock_create_article)

        response = client.post(self.url, json=article)

        expect(response.status_code).to.be.equal(status.HTTP_201_CREATED)
        want = article
        want["slug"] = "fake-article"
        want["created_at"] = now
        want["updated_at"] = now
        expect(response.json()).to.be.equal(want)

    def test_it_can_not_create_an_existing_article(self, monkeypatch):
        url = '/articles'
        article = {'title': 'Fake Article', 'description': 'Description', 'body': 'Something', 'author_id': 1}

        def mock_create_article(*args, **kwargs):
            raise ArticleExistedException("the article with slug {} already exists".format("fake-article"))

        monkeypatch.setattr(ArticleService, "create_article", mock_create_article)

        response = client.post(url, json=article)

        expect(response.status_code).to.be.equal(status.HTTP_409_CONFLICT)
        want = {"message": "the article with slug fake-article already exists"}
        expect(response.json()).to.be.equal(want)
