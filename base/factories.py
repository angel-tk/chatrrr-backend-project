import factory
from django.contrib.auth.models import User
from base.models import Room, Topic, Message

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass')

class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Faker('sentence', nb_words=3)  

class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room
    host = factory.SubFactory(UserFactory)
    topic = factory.SubFactory(TopicFactory)
    name = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=200)

class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message
    user = factory.SubFactory(UserFactory)
    room = factory.SubFactory(RoomFactory)
    body = factory.Faker('sentence', nb_words=10)
