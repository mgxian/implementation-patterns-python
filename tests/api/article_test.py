import unittest
import requests
import uvicorn
from controller.app import app
from fastapi import status
from grappa import expect
from multiprocessing import Process

host = '127.0.0.1'
port = 6666


class TestArticle(unittest.TestCase):
    def setUp(self):
        self.proc = Process(
            target=uvicorn.run,
            args=(app,),
            kwargs={
                "host": host,
                "port": port,
                "log_level": "info"
            },
            daemon=True
        )
        self.proc.start()

    def tearDown(self):
        self.proc.terminate()

    def test_it_can_create_article(self):
        url = "http://{}:{}{}".format(host, port, "/articles")
        article_request = {'title': 'Fake Article', 'description': 'Description', 'body': 'Something', 'author_id': 1}
        response = requests.post(url, json=article_request)
        expect(response.status_code).to.be.equal(status.HTTP_201_CREATED)
