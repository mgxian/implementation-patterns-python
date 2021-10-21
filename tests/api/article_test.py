import time
import unittest
import requests
import uvicorn
from controller.app import app
from fastapi import status
from grappa import expect
from threading import Thread

host = '127.0.0.1'
port = 6666


class TestArticle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        thread = Thread(
            target=uvicorn.run,
            args=(app,),
            kwargs={
                "host": host,
                "port": port,
            },
            daemon=True
        )
        thread.start()
        time.sleep(0.1)

    def setUp(self):
        self.url = "http://{}:{}{}".format(host, port, "/articles")
        self.article_request = {'title': 'Fake Article', 'description': 'Description', 'body': 'Something',
                                'author_id': 1}

    def test_it_can_create_article(self):
        response = requests.post(self.url, json=self.article_request)
        expect(response.status_code).to.be.equal(status.HTTP_201_CREATED)
        got = response.json()
        expect(got['slug']).to.be.equal('fake-article')
        expect(got['title']).to.be.equal(self.article_request['title'])
        expect(got['description']).to.be.equal(self.article_request['description'])
        expect(got['body']).to.be.equal(self.article_request['body'])
        expect(got['author_id']).to.be.equal(self.article_request['author_id'])
        expect(got['created_at']).not_to.be.equal(None)
        expect(got['updated_at']).not_to.be.equal(None)

    def test_it_can_not_create_an_existing_article(self):
        response = requests.post(self.url, json=self.article_request)
        expect(response.status_code).to.be.equal(status.HTTP_409_CONFLICT)
        got = response.json()
        expect(got['message']).to.be.equal("the article with slug {} already exists".format("fake-article"))
