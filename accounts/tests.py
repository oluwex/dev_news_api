from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Profile


# Create your tests here.

class AccountTests(APITestCase):

    def setUp(self):
        password = 'Abcabc123'
        user1 = User.objects.create_user(username='jeffa@mail.com', email='jeffa@mail.com', password=password)
        user2 = User.objects.create_user(username='otto@mail.com', email='otto@mail.com', password=password)

        profile1 = Profile.objects.create(
            user=user1,
            name="Jeff Dunham",
            bio="Random bio kan noni"
        )
        profile2 = Profile.objects.create(
            user=user2,
            name="Otto Octavius",
            bio="Renowed scientist and passionate reader."
        )

    def test_create_account(self):
        """
        Test to ensure a new user can register
        """
        url = reverse('accounts-api:register')
        data = {'name': "Habeeb Oluwo", 'email': "omotee24@gmail.com", 'password': "Abcabc123", 'bio': 'Down to earth individual'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(email='omotee24@gmail.com').profile.name, 'Habeeb Oluwo')

    def test_login_valid(self):
        """
        Testing user login
        """
        url = reverse('accounts-api:login')
        data = {'email': "otto@mail.com", 'password': 'Abcabc123'}
        response = self.client.post(url, data, format='json')
        self.assertTrue(status.is_success(response.status_code))
        self.assertIsNotNone(response.data.get('email'))
        self.assertEqual(response.data.get('email'), 'otto@mail.com')
        self.assertIsNotNone(response.data.get('token'))
        self.assertTrue(response.data.get('token').isalnum())

    def test_login_invalid(self):
        """
        Testing invalid login
        """
        url = reverse('accounts-api:login')
        data = {'email': "omotee24@gmail.com", 'password': 'Abcabc123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_accounts_unauthorized(self):
        """
        Tests the list authors API view for unauthorized user
        """
        url = reverse('accounts-api:users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_accounts_authorized(self):
        """
        Tests the list authors API view for authorized user
        """
        User.objects.create_user(email='omotee24@gmail.com', username='omotee24@gmail.com', password="Abcabc123")
        url = reverse('accounts-api:users')
        self.client.login(username='jeffa@mail.com', password='Abcabc123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_login(self):
        """
        Tests login endpoint
        """
        user_token = Token.objects.get(user__username='jeffa@mail.com')
        url = reverse('accounts-api:login')
        data = {'email':'jeffa@mail.com', 'password':'Abcabc123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('token'), user_token.key)

