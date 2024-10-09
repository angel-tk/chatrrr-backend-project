from django.test import TestCase
from base.factories import RoomFactory, TopicFactory, UserFactory, MessageFactory

class ModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.topic = TopicFactory(name='Test Topic')
        self.room = RoomFactory(host=self.user, topic=self.topic, name="Test Room", description="Room Description")

    def test_topic_str(self):
        self.assertEqual(str(self.topic), 'Test Topic')

    def test_room_str(self):
        self.assertEqual(str(self.room), 'Test Room')

    def test_message_str(self):
        message = MessageFactory(user=self.user, room=self.room, body="Test Message Body")
        self.assertEqual(str(message), "Test Message Body"[0:50])
