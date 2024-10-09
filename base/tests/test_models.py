from django.test import TestCase
from base.models import Room, Topic, Message
from django.contrib.auth.models import User

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(name='Test Topic')
        self.room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name="Test Room",
            description="Room Description"
        )

    def test_topic_str(self):
        self.assertEqual(str(self.topic), 'Test Topic')

    def test_room_str(self):
        self.assertEqual(str(self.room), 'Test Room')

    def test_message_str(self):
        message = Message.objects.create(user=self.user, room=self.room, body="Test Message Body")
        self.assertEqual(str(message), "Test Message Body"[0:50])
