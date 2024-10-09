from django.test import TestCase, Client
from django.urls import reverse
from base.models import Room, Message 
from base.factories import UserFactory, RoomFactory, TopicFactory, MessageFactory

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = UserFactory(username='testuser1', password='testpass1')
        self.user2 = UserFactory(username='testuser2', password='testpass2')
        self.topic = TopicFactory(name='Test Topic')
        self.room = RoomFactory(host=self.user1, topic=self.topic, name='Test Room', description='Room Description')
        self.message = MessageFactory(user=self.user1, room=self.room, body='Test message')

        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.room_url = reverse('room', args=[self.room.id])
        self.create_room_url = reverse('create-room')
        self.delete_room_url = reverse('delete-room', args=[self.room.id])
        self.update_room_url = reverse('update-room', args=[self.room.id])

class AuthenticationTests(BaseTestCase):
    def test_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')

    def test_login_post_valid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser1',
            'password': 'testpass1'
        })
        self.assertRedirects(response, self.home_url)

    def test_login_post_invalid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser1',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username OR password does not exist')

    def test_logout(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, self.home_url)

class HomeAndRoomTests(BaseTestCase):
    def test_home_page(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')
        self.assertContains(response, self.room.name)

    def test_room_page(self):
        response = self.client.get(self.room_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/room.html')
        self.assertContains(response, self.room.name)
        self.assertContains(response, self.message.body)

class RoomCRUDTests(BaseTestCase):
    def test_create_room_authenticated(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.post(self.create_room_url, {
            'name': 'New Room',
            'description': 'New Description',
            'topic': 'New Topic',
        })
        self.assertRedirects(response, self.home_url)
        self.assertTrue(Room.objects.filter(name='New Room').exists())

    def test_update_room_as_host(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.post(self.update_room_url, {
            'name': 'Updated Room',
            'description': 'Updated Description',
            'topic': 'Test Topic',
        })
        self.assertRedirects(response, self.home_url)
        self.room.refresh_from_db()
        self.assertEqual(self.room.name, 'Updated Room')

    def test_update_room_as_non_host(self):
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.post(self.update_room_url, {
            'name': 'Updated Room',
            'description': 'Updated Description',
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_room_as_host(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.post(self.delete_room_url)
        self.assertRedirects(response, self.home_url)
        self.assertFalse(Room.objects.filter(id=self.room.id).exists())

    def test_delete_room_as_non_host(self):
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.post(self.delete_room_url)
        self.assertEqual(response.status_code, 403)

class MessageTests(BaseTestCase):
    def test_delete_message_as_author(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.post(reverse('delete-message', args=[self.message.id]))
        self.assertRedirects(response, self.home_url)
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())

    def test_delete_message_as_non_author(self):
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.post(reverse('delete-message', args=[self.message.id]))
        self.assertEqual(response.status_code, 403)
