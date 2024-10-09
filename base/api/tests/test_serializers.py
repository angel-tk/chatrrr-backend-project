from django.test import TestCase
from base.api.serializers import RoomSerializer
from base.factories import UserFactory, TopicFactory, RoomFactory

class RoomSerializerTests(TestCase):
    def setUp(self):
        self.user = UserFactory(username='testuser', password='testpass')
        self.topic = TopicFactory(name='Test Topic')
        self.room = RoomFactory(host=self.user, topic=self.topic, name='Test Room', description='Test Room Description')

    def test_room_serialization(self):
        serializer = RoomSerializer(self.room)
        data = serializer.data
        
        self.assertEqual(data['name'], self.room.name)
        self.assertEqual(data['description'], self.room.description)
        self.assertEqual(data['host'], self.room.host.id)
        self.assertEqual(data['topic'], self.room.topic.id)

    def test_room_deserialization(self):
        room_data = {
            'host': self.user.id,
            'topic': self.topic.id,
            'name': 'New Room',
            'description': 'New Room Description'
        }
        
        serializer = RoomSerializer(data=room_data)
        self.assertTrue(serializer.is_valid())
        room = serializer.save()
        
        self.assertEqual(room.name, 'New Room')
        self.assertEqual(room.description, 'New Room Description')
        self.assertEqual(room.host, self.user)
        self.assertEqual(room.topic, self.topic)

    def test_room_serializer_invalid_data(self):
        invalid_data = {
            'host': self.user.id,
            'topic': None,
            'name': '',
        }
        
        serializer = RoomSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
