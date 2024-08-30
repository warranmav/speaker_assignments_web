import unittest
from app import create_app, db
from app.models import Record

class DeleteEntryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

        # Create a record to test deletion
        self.record = Record(name='Test User')
        db.session.add(self.record)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_request(self):
        response = self.client.get('/delete/entry')
        self.assertEqual(response.status_code, 200)

    def test_delete_existing_record(self):
        response = self.client.post('/delete/entry', data={'record_id': self.record.id})
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion

        follow_up_response = self.client.get('/delete/entry')
        self.assertIn(b"Name &#39;Test User&#39; deleted from the database.", follow_up_response.data)

    def test_delete_non_existing_record(self):
        response = self.client.post('/delete/entry', data={'record_id': 9999})
        self.assertEqual(response.status_code, 302)  # Redirect after trying to delete a non-existing record
        follow_up_response = self.client.get('/delete/entry')
        self.assertIn(b'Record not found.', follow_up_response.data)

if __name__ == '__main__':
    unittest.main()
