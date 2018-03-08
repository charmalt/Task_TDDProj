from unittest import TestCase

from user_submit_post import submit_post
from user_submit_post.config import host, port
import psycopg2
from user_submit_post.submit_post import db, list


# User hears about new organiser app
class TestApp(TestCase):

    def setUp(self):
        self.app = submit_post.app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass
    # TODO: Drop Table on completion if necessary

    # User goes to check out the homepage.
    def test_page_response(self):
        url = 'http://{}:{}/'.format(host, port)
        response = self.app.get(url)
        self.assertEqual('200 OK', response.status)

    def test_home_page_returns_correct_html(self):
        url = 'http://{}:{}/'.format(host, port)
        response = self.app.get(url)
        # html = response.get_data(as_text=True)
        self.assertEqual(b'Welcome to To Do List.', response.data)

    # User is asked to enter a to-do item.
    def test_add_task_returns_correct_html(self):
        url = 'http://{}:{}/add_task'.format(host, port)
        response = self.app.get(url)
        html = response.get_data(as_text=True)
        self.assertIn('<form', html)
        self.assertIn('<input', html)

    # User enters "Buy a new helmet for cycling" into text box and hits submit
    # On hitting enter, page updates and lists
    # "Added new item to To-Do List: Buy a new helmet for cycling" as an item in to-do list
    def test_home_page_accepts_post_request(self):
        db.create_all()
        response = self.app.post('/add_task', data={"task": "Buy a new helmet for cycling1"})
        self.assertEqual('200 OK', response.status)
        self.assertEqual('Added new item to Task List.', response.get_data(as_text=True))
        id = list.query.all()
        db.session.close()
    # TODO: Delete the added row since this is a test!

    def test_postgres_table_connectable(self):
        conn = False
        connection = psycopg2.connect(
            database="flaskexample",
            user="CCHETCU3", password="Blue24",
            host='localhost', port=5432,
        )
        if connection is not None:
            conn = True
        self.assertTrue(conn)
        connection.close()

    def test_check_save_to_database(self):
        db.create_all()
        test_task = list('Buy food for puppy')
        db.session.add(test_task)
        response = str(list.query.all())
        self.assertIn('Buy food for puppy', response)
        db.session.rollback()
        db.session.close()


