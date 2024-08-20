import unittest
from app import create_app, db
from app.models import Record

class NameManagementTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test database and test client."""
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data()

    def tearDown(self):
        """Tear down the test database."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_test_data(self):
        """Add test data to the database."""
        record = Record(name='Test User')
        db.session.add(record)
        db.session.commit()

    def test_add_name(self):
        """Test adding a new name to the database."""
        response = self.client.post('/name_management/add', data={'name': 'New User'})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        response = self.client.get('/name_management/add')
        self.assertIn(b'New User', response.data)  # Check if the name is in the page

    def test_add_existing_name(self):
        """Test adding a name that already exists."""
        response = self.client.post('/name_management/add', data={'name': 'Test User'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/name_management/add')
        self.assertIn(b'Test User', response.data)  # Check if the name exists in the flash message

    def test_delete_name(self):
        """Test deleting a name from the database."""
        # Adding a name to delete
        record = Record(name='Delete User')
        db.session.add(record)
        db.session.commit()

        record_id = record.id
        response = self.client.post('/name_management/delete', data={'record_id': record_id})
        self.assertEqual(response.status_code, 302)

        # Verify that the name is no longer in the database
        deleted_record = db.session.get(Record, record_id)
        self.assertIsNone(deleted_record)  # Ensure the record is None, meaning it's deleted


    def test_view_database(self):
        """Test viewing the names in the database."""
        response = self.client.get('/name_management/view')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

if __name__ == '__main__':
    unittest.main()
