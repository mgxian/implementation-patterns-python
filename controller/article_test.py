import time
from grappa import expect
from controller.app import app
from fastapi.testclient import TestClient
from fastapi import status

from domain.model.article import Article
from domain.service.article import ArticleService

client = TestClient(app)


class TestArticle:
    def test_it_can_create_an_article(self, monkeypatch):
        url = '/articles'
        article = {'title': 'Fake Article', 'description': 'Description', 'body': 'Something', 'author_id': 1}

        now = time.time()

        def mock_create_article(*args, **kwargs):
            result = Article("fake-article", "Fake Article", "Description", "Something", 1)
            result.created_at = now
            result.updated_at = now
            return result

        monkeypatch.setattr(ArticleService, "create_article", mock_create_article)

        response = client.post(url, json=article)

        expect(response.status_code).to.be.equal(status.HTTP_201_CREATED)
        want = article
        want["slug"] = "fake-article"
        want["created_at"] = now
        want["updated_at"] = now
        expect(response.json()).to.be.equal(want)
