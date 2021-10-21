import time

from grappa import expect
from unittest.mock import Mock

from domain.service.article import ArticleService


class TestArticle:
    def test_it_can_create_an_article(self):
        clock = Mock()
        now = time.time()
        clock.now.return_value = now
        article_repository = Mock()
        article_service = ArticleService(article_repository, clock)

        title = 'Fake Article'
        description = 'Description'
        body = 'Something'
        author_id = 1

        def side_effect(*args):
            return args[0]

        article_repository.save.side_effect = side_effect

        got = article_service.create_article(title, description, body, author_id)

        expect(got.slug).to.be.equal('fake-article')
        expect(got.title).to.be.equal(title)
        expect(got.description).to.be.equal(description)
        expect(got.body).to.be.equal(body)
        expect(got.author_id).to.be.equal(author_id)
        expect(got.created_at).to.be.equal(now)
        expect(got.updated_at).to.be.equal(now)
