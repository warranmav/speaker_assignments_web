import unittest
from app import create_app, db

class AddNameTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')  # Use the testing configuration
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_name(self):
        response = self.client.post('/add/name', data={'name': 'New User'})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        redirected_response = self.client.get(response.location)  # Follow the redirect
        self.assertIn(b"Name &#39;New User&#39; added to database.", redirected_response.data)

    def test_add_existing_name(self):
        # Add a name first
        self.client.post('/add/name', data={'name': 'Test User'})
        # Try to add the same name again
        response = self.client.post('/add/name', data={'name': 'Test User'})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        redirected_response = self.client.get(response.location)  # Follow the redirect
        self.assertIn(b"Name &#39;Test User&#39; already exists in the database.", redirected_response.data)

    def test_add_empty_name(self):
        # Attempt to add a name without providing a name
        response = self.client.post('/add/name', data={'name': ''})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        redirected_response = self.client.get(response.location)  # Follow the redirect
        self.assertIn(b'Name is required!', redirected_response.data)

if __name__ == '__main__':
    unittest.main()
