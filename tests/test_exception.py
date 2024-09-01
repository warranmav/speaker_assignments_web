# tests/test_exception.py

import unittest
from app import create_app, db
from app.models import Record

class ExceptionTestCase(unittest.TestCase):

    def setUp(self):
        # Setup the Flask test client and the database for testing
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        # Add a sample record to the database
        self.record = Record(name="Test User")
        db.session.add(self.record)
        db.session.commit()

    def tearDown(self):
        # Remove the session and drop all tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_exception(self):
        # Test adding an exception
        response = self.client.post('/exception/add', data={
            'record_id': self.record.id,
            'exception': 'Health'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        updated_record = Record.query.get(self.record.id)
        self.assertEqual(updated_record.exception, 'Health')
        self.assertIsNone(updated_record.date_last_spoken)

    def test_update_exception(self):
        # Test updating an exception
        self.record.exception = 'Inactive'
        db.session.commit()

        response = self.client.post('/exception/update', data={
            'record_id': self.record.id,
            'exception': 'Refusal'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        updated_record = Record.query.get(self.record.id)
        self.assertEqual(updated_record.exception, 'Refusal')
        self.assertIsNone(updated_record.date_last_spoken)

    def test_remove_exception(self):
        # Test removing an exception
        self.record.exception = 'Health'
        db.session.commit()

        response = self.client.post('/exception/remove', data={
            'record_id': self.record.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        updated_record = Record.query.get(self.record.id)
        self.assertIsNone(updated_record.exception)
        self.assertTrue(updated_record.included_in_pool)

    def test_set_available(self):
        # Test setting the record as available
        self.record.exception = 'Inactive'
        db.session.commit()

        response = self.client.post('/exception/available', data={
            'record_id': self.record.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        updated_record = Record.query.get(self.record.id)
        self.assertEqual(updated_record.exception, 'Available')
        self.assertTrue(updated_record.included_in_pool)

if __name__ == '__main__':
    unittest.main()
