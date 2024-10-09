from django.test import TestCase
from base.forms import RoomForm, UserForm
from base.models import Topic
from django.contrib.auth.models import User

class RoomFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(name='Test Topic')

    def test_room_form_valid_data(self):
        form_data = {
            'name': 'Test Room',
            'topic': self.topic.id,
            'description': 'This is a test room',
        }
        form = RoomForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_room_form_invalid_data(self):
        form_data = {
            'name': '',
            'topic': self.topic.id,
            'description': 'This room has no name',
        }
        form = RoomForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_room_form_excludes_fields(self):
        form = RoomForm()
        self.assertNotIn('host', form.fields)
        self.assertNotIn('participants', form.fields)

from django.test import TestCase
from base.forms import UserForm
from django.contrib.auth.models import User

class UserFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')

    def test_user_form_valid_data(self):
        form_data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_form_invalid_data(self):
        form_data = {
            'username': '',
            'email': 'newemail@example.com'
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_user_form_email_validation(self):
        form_data = {
            'username': 'newusername',
            'email': 'not-an-email'
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)