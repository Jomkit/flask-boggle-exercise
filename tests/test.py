from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

#For testing
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def setUp(self):
        """set up each test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    # TODO -- write tests for every view function
    def test_homepage(self):
        with self.client:

            resp = self.client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Score: <span id="score">0</span></p>', html)
            self.assertIn('<p>High Score: <span id="hi-score">0</span></p>', html)
            self.assertIn('board', session)
            self.assertEqual(session['num_played'], 0)

    def test_check_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["D","O","G","G","G"],
                                 ["D","O","G","G","G"],
                                 ["D","O","G","G","G"],
                                 ["D","O","G","G","G"],
                                 ["D","O","G","G","G"]]
            
            # if word is on board
            resp = self.client.post('/check-word', json={'word':'dog'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('ok', html)

            # if word not on board
            resp = self.client.post('/check-word', json={'word':'cat'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('not-on-board', html)

            # if not word
            resp = self.client.post('/check-word', json={'word':'asdf'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('not-word', html)

    def test_store_statistics(self):
        with self.client as client:
            # initial conditions
            resp = self.client.post('/store-statistics', json={'score':5})
            html = resp.get_data(as_text=True)

            self.assertEqual(session['num_played'], 1)
            self.assertEqual(session['curr-hi-score'], 5)
            self.assertIn('5',html)

            