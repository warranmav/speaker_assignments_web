import unittest
from unittest.mock import patch
from datetime import datetime
from app import create_app, db
from app.models import TalkAssignment, Record, Theme, Topic

class MainViewTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test app with the testing configuration
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create the database and add some sample data
        db.create_all()

        # Create sample records
        record1 = Record(id=1, name="Speaker 1")
        record2 = Record(id=2, name="Speaker 2")
        record3 = Record(id=3, name="Speaker 3")

        # Create sample themes and topics
        theme = Theme(id=1, name="Theme 1")
        topic = Topic(id=1, name="Topic 1", theme_id=1)

        # Add test data - assign speaker_id as per the Record instances
        assignment1 = TalkAssignment(
            id=1,
            speaker_id=1,
            date=datetime(2024, 8, 1),
            speaker_pos="Main Speaker",
            talk_length="30 minutes",
            theme_id=1,
            topic_id=1
        )
        assignment2 = TalkAssignment(
            id=2,
            speaker_id=2,
            date=datetime(2024, 8, 15),
            speaker_pos="Supporting Speaker",
            talk_length="15 minutes",
            theme_id=1,
            topic_id=1
        )
        assignment3 = TalkAssignment(
            id=3,
            speaker_id=3,
            date=datetime(2024, 9, 1),  # This assignment is for the next month
            speaker_pos="Main Speaker",
            talk_length="30 minutes",
            theme_id=1,
            topic_id=1
        )

        db.session.add_all([record1, record2, record3, theme, topic, assignment1, assignment2, assignment3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.routes.main.datetime')  # Patch datetime in the main module
    def test_index_view(self, mock_datetime):
        # Mock the date to ensure consistency in the test
        mock_datetime.today.return_value = datetime(2024, 8, 10)
        mock_datetime.strftime = datetime.strftime

        # Call the index route
        response = self.client.get('/')

        # Check that the request succeeded
        self.assertEqual(response.status_code, 200)

        # Verify that the correct assignments are shown
        self.assertIn(b'Speaker 1', response.data)
        self.assertIn(b'Speaker 2', response.data)
        self.assertNotIn(b'Speaker 3', response.data)  # This one should not appear as it's in the next month

if __name__ == '__main__':
    unittest.main()
