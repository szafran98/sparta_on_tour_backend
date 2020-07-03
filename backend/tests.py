from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Event, Participant
import datetime


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"email": "test@localhost.com", "username": "testuser",
                "password": "testpass", "password1": "testpass"}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username='testcase').username, 'testcase')


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

    def test_user_login(self):
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post('/auth/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_no_user(self):
        data = {"username": "baduser", "password": "badpass"}
        response = self.client.post('/auth/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testadmin', password='adminpass', is_staff=True)
        self.token = Token.objects.create(user=self.user)
        self.user_authentication()

    def user_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_event(self):
        data = {"title": "test_title", "description": "test_description",
                "date": "test_date", "can_be_joined_to": "test_date_2",
                "image_link": "http://grafika.pl"}

        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().title, 'test_title')

    def test_create_event_user_not_allowed(self):
        self.client.credentials()
        data = {"title": "test_title", "description": "test_description",
                "date": "test_date", "can_be_joined_to": "test_date_2",
                "image_link": "http://grafika.pl"}

        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Event.objects.count(), 0)

    def test_create_event_no_data(self):
        data = {"title": "", "description": "",
                "date": datetime.datetime(2020, 7, 20, 20, 0, 0),
                "can_be_joined_to": datetime.datetime(2020, 7, 19, 20, 0, 0),
                "image_link": ""}

        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(Event.objects.count(), 0)

    def test_join_event(self):
        event_to_join = Event.objects.create(
            title='testevent',
            description="description",
            date=datetime.datetime(2020, 7, 20, 20, 0, 0),
            can_be_joined_to=datetime.datetime(2020, 7, 19, 20, 0, 0),
            image_link='http://test.pl'
        )
        data = {"first_name": "testname", "last_name": "testlastname",
                "pesel": 0, "joined_event": event_to_join.id, "user": self.token}

        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Participant.objects.get(user=self.user))

    def test_join_event_no_data(self):
        event_to_join = Event.objects.create(
            title='testevent',
            description="description",
            date=datetime.datetime(2020, 7, 20, 20, 0, 0),
            can_be_joined_to=datetime.datetime(2020, 7, 19, 20, 0, 0),
            image_link='http://test.pl'
        )
        data = {"first_name": "", "last_name": "",
                "pesel": "", "joined_event": event_to_join.id, "user": self.token}

        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(Event.objects.count(), 0)


class ParticipantViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testuser')
        self.token = Token.objects.create(user=self.user)

    def test_get_events_joined_by_user(self):
        event = Event.objects.create(
            title='testevent',
            description="description",
            date=datetime.datetime(2020, 7, 20, 20, 0, 0),
            can_be_joined_to=datetime.datetime(2020, 7, 19, 20, 0, 0),
            image_link='http://test.pl'
        )
        Participant.objects.create(
            first_name='testname',
            last_name='testlastname',
            pesel=123,
            joined_event=event,
            user=self.user
        )

        response = self.client.get('/api/participants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'].event.id, 1)
