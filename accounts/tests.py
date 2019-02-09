from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Test to ensure a new user can register
        """
        url = reverse('accounts-api:register')
        data = {'name': "Habeeb Oluwo", 'email': "omotee24@gmail.com", 'password': "Abcabc123", 'bio': 'Down to earth individual'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().profile.name, 'Habeeb Oluwo')
