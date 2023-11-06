from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function
    def test_root(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Score: <span id="score">0</span></p>', html)

    def test_check_word(self):
        with app.test_client() as client:
            resp = client.post('/check-word', data={'word'='run'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            