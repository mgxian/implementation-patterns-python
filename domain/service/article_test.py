import time
import pytest

from grappa import expect
from unittest.mock import Mock
from unittest import TestCase

from domain.service.article import ArticleService, ArticleExistedException


class TestArticle(TestCase):
    def setUp(self):
        now = time.time()
        self.clock = Mock()
        self.clock.now.return_value = now
        self.article_repository = Mock()
        self.article_service = ArticleService(self.article_repository, self.clock)

    def test_it_can_create_an_article(self):
        title = 'Fake Article'
        description = 'Description'
        body = 'Something'
        author_id = 1

        def side_effect(*args):
            return args[0]

        self.article_repository.save.side_effect = side_effect
        self.article_repository.exists_by_slug.return_value = False

        got = self.article_service.create_article(title, description, body, author_id)

        expect(got.slug).to.be.equal('fake-article')
        expect(got.title).to.be.equal(title)
        expect(got.description).to.be.equal(description)
        expect(got.body).to.be.equal(body)
        expect(got.author_id).to.be.equal(author_id)
        expect(got.created_at).to.be.equal(self.clock.now())
        expect(got.updated_at).to.be.equal(self.clock.now())

    def test_it_can_not_create_an_existing_article(self):
        title = 'Fake Article'
        description = 'Description'
        body = 'Something'
        author_id = 1
        self.article_repository.exists_by_slug.return_value = True

        with pytest.raises(ArticleExistedException):
            self.article_service.create_article(title, description, body, author_id)
