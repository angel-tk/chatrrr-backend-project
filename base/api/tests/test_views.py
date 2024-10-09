from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from base.models import Room, Topic
from django.contrib.auth.models import User

class RoomApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(name='Test Topic')
        self.room1 = Room.objects.create(
            host=self.user, 
            topic=self.topic, 
            name="Room 1", 
            description="First test room"
        )
        self.room2 = Room.objects.create(
            host=self.user, 
            topic=self.topic, 
            name="Room 2", 
            description="Second test room"
        )

    def test_get_routes(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            'GET/api/',
            'GET/api/rooms',
            'GET/api/rooms/:id',
        ])

    def test_get_rooms(self):
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.room2.name)
        self.assertEqual(response.data[1]['name'], self.room1.name)

    def test_get_single_room(self):
        response = self.client.get(f'/api/rooms/{self.room1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.room1.name)

    def test_get_single_room_not_found(self):
        response = self.client.get('/api/rooms/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
