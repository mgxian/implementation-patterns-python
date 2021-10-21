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
    def setUp(self):
        self.thread = Thread(
            target=uvicorn.run,
            args=(app,),
            kwargs={
                "host": host,
                "port": port,
            },
            daemon=True
        )
        self.thread.start()
        time.sleep(0.1)

    def test_it_can_create_article(self):
        url = "http://{}:{}{}".format(host, port, "/articles")
        article_request = {'title': 'Fake Article', 'description': 'Description', 'body': 'Something', 'author_id': 1}
        response = requests.post(url, json=article_request)
        expect(response.status_code).to.be.equal(status.HTTP_201_CREATED)
        got = response.json()
        expect(got['slug']).to.be.equal('fake-article')
        expect(got['title']).to.be.equal(article_request['title'])
        expect(got['description']).to.be.equal(article_request['description'])
        expect(got['body']).to.be.equal(article_request['body'])
        expect(got['author_id']).to.be.equal(article_request['author_id'])
        expect(got['created_at']).not_to.be.equal(None)
        expect(got['updated_at']).not_to.be.equal(None)
