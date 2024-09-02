import unittest
from unittest.mock import patch
from datetime import datetime
from app import create_app, db
from app.models import TalkAssignment, Record, Theme, Topic

class MainViewTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test app with the testing configuration
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create the database and add some sample data
        db.create_all()

        # Create sample records
        record1 = Record(name="Speaker 1")
        record2 = Record(name="Speaker 2")
        record3 = Record(name="Speaker 3")

        # Create sample themes and topics
        theme = Theme(name="Theme 1")
        topic = Topic(name="Topic 1", theme=theme)  # Associate the topic with the theme

        # Add records, theme, and topic to the session to generate their IDs
        db.session.add_all([record1, record2, record3, theme, topic])
        db.session.commit()

        # Add test data - assign speaker_id as per the Record instances
        assignment1 = TalkAssignment(
            speaker_id=record1.id,
            date=datetime(2024, 8, 1),
            speaker_pos="Main Speaker",
            talk_length="30 minutes",
            theme_id=theme.id,
            topic_id=topic.id
        )
        assignment2 = TalkAssignment(
            speaker_id=record2.id,
            date=datetime(2024, 8, 15),
            speaker_pos="Supporting Speaker",
            talk_length="15 minutes",
            theme_id=theme.id,
            topic_id=topic.id
        )
        assignment3 = TalkAssignment(
            speaker_id=record3.id,
            date=datetime(2024, 9, 1),  # This assignment is for the next month
            speaker_pos="Main Speaker",
            talk_length="30 minutes",
            theme_id=theme.id,
            topic_id=topic.id
        )

        db.session.add_all([assignment1, assignment2, assignment3])
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
