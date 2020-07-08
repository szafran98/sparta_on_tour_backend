from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"email": "test@localhost.com", "first_name": "testname",
                'last_name': 'testlastname', 'pesel': 123,
                "password": "testpass", "password2": "testpass"}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.first().first_name, 'testname')


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

    def test_user_login(self):
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post('/auth/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_no_user(self):
        data = {"username": "baduser", "password": "badpass"}
        response = self.client.post('/auth/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)