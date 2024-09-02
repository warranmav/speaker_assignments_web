import unittest
from app import create_app, db
from app.models import Record, TalkAssignment
from datetime import datetime, timedelta

class AssignTalkTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test database and test client."""
        self.app = create_app('testing')  # Use the TestingConfig for this test case
        self.client = self.app.test_client()  # Create a test client to make requests
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()  # Create the tables in the in-memory database
        self.add_test_data()  # Add test data to the in-memory database

    def tearDown(self):
        """Tear down the test database."""
        db.session.remove()
        db.drop_all()  # Drop all tables after the test case is done
        self.app_context.pop()

    def add_test_data(self):
        """Add test data to the database."""
        # Add records with varying dates and exceptions
        record1 = Record(name='John Doe', exception=None)
        record2 = Record(name='Jane Smith', exception='Available')
        record3 = Record(name='Alice Johnson', exception='Not Available')

        db.session.add_all([record1, record2, record3])
        db.session.commit()

        # Assign past talks to some records
        past_date = datetime.today() - timedelta(days=200)
        talk1 = TalkAssignment(speaker_id=record1.id, date=past_date, speaker_pos='First', talk_length=10)
        talk2 = TalkAssignment(speaker_id=record3.id, date=datetime.today(), speaker_pos='Second', talk_length=5)

        db.session.add_all([talk1, talk2])
        db.session.commit()

    def test_assign_talk_eligible_names(self):
        """Test that only eligible names are listed for talk assignment."""
        response = self.client.get('/assign/talk')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)  # John should be eligible
        self.assertIn(b'Jane Smith', response.data)  # Jane should be eligible
        self.assertNotIn(b'Alice Johnson', response.data)  # Alice should be excluded

    def test_assign_talk_post(self):
        """Test assigning a talk via POST request."""
        response = self.client.post('/assign/talk', data={
            'record_id': 1,  # Assuming John Doe's ID is 1
            'date': '2024-08-20',
            'speaker_pos': 'First',
            'talk_length': '10'
        })
        self.assertEqual(response.status_code, 302)  # A redirect indicates success
        self.assertIn(b'Talk assigned successfully', self.client.get('/assign/talk').data)

if __name__ == '__main__':
    unittest.main()
