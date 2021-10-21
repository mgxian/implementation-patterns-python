from domain.model.article import ArticleRepository, Article


class ArticleRepositoryDB(ArticleRepository):
    def __init__(self):
        self._data = {}

    def save(self, article: Article) -> Article:
        self._data[article.slug] = article
        return article
