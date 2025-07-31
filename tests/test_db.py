import os
import sys

os.environ['TESTING'] = 'true'

# Ensure the application package can be imported when running tests directly
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest
from peewee import *
from app import TimelinePost

MODELS = [TimelinePost]
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe',
            email='john@example.com', content="Hello world, I'm John!")
        second_post = TimelinePost.create(name='Jane Doe',
            email='jane@example.com', content="Hello world, I'm Jane!")

        posts = TimelinePost.select().order_by(TimelinePost.id)
        self.assertEqual(posts.count(), 2)

        # Assert the content of the first post
        self.assertEqual(posts[0].name, 'John Doe')
        self.assertEqual(posts[0].email, 'john@example.com')
        self.assertEqual(posts[0].content, "Hello world, I'm John!")

        # Assert the content of the second post
        self.assertEqual(posts[1].name, 'Jane Doe')
        self.assertEqual(posts[1].email, 'jane@example.com')
        self.assertEqual(posts[1].content, "Hello world, I'm Jane!")

if __name__ == '__main__':
    unittest.main() 