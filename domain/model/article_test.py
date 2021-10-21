import time

from grappa import expect

from domain.model.article import Article


class TestArticle:
    def setup(self):
        self.slug = 'fake-article'
        self.title = 'Fake Article'
        self.description = 'Description'
        self.body = 'Something'
        self.author_id = 1
        self.article = Article(self.slug, self.title, self.description, self.body, self.author_id)

    def test_it_can_create_article(self):
        expect(self.article.slug).to.be.equal(self.slug)
        expect(self.article.title).to.be.equal(self.title)
        expect(self.article.description).to.be.equal(self.description)
        expect(self.article.body).to.be.equal(self.body)
        expect(self.article.author_id).to.be.equal(self.author_id)
        expect(self.article.created_at).to_not.be.equal(None)
        expect(self.article.updated_at).to_not.be.equal(None)
        expect(self.article.created_at).to.be.equal(self.article.updated_at)

    def test_it_can_set_created_at(self):
        now = time.time()
        self.article.created_at = now
        expect(self.article.created_at).to.be.equal(now)

    def test_it_can_set_updated_at(self):
        now = time.time()
        self.article.updated_at = now
        expect(self.article.updated_at).to.be.equal(now)
