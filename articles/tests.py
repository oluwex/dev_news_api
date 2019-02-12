from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Profile
from .models import Article

# Create your tests here.


class ArticleTest(APITestCase):
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

        self.article1 = Article.objects.create(title="Old title", content="Old content", author=profile1)
        self.article2 = Article.objects.create(title="Old title", content="Old content", author=profile2)

    def test_create_article(self):
        login_url = reverse('accounts-api:login')
        login_data = {'email': "jeffa@mail.com", 'password': 'Abcabc123'}
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data.get('token', "")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('articles-api:create_article')
        data = {'title': "Test 1", "content": "Content 1"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    def test_create_article_by_unauthorized_user(self):
        url = reverse('articles-api:create_article')
        data = {'title': "Test 1", "content": "Content 1"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_list_view_by_authorized_user(self):
        login_url = reverse('accounts-api:login')
        login_data = {'email': "jeffa@mail.com", 'password': 'Abcabc123'}
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data.get('token', "")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('articles-api:view_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_article_list_view_by_unauthorized_user(self):
        url = reverse('articles-api:view_articles')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_retrieve_by_authorized_user(self):
        login_url = reverse('accounts-api:login')
        login_data = {'email': "jeffa@mail.com", 'password': 'Abcabc123'}
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data.get('token', "")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('articles-api:retrieve_article', kwargs={'slug': self.article1.slug})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.article1.title)

    def test_article_retrieve_by_unauthorized_user(self):
        url = reverse('articles-api:retrieve_article', kwargs={'slug': self.article1.slug})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_update_by_unauthorized_user(self):
        url = reverse('articles-api:update_article', kwargs={'slug': self.article1.slug})
        data = {'title': self.article2.title, 'content': 'Content has been updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_update_by_author(self):
        login_url = reverse('accounts-api:login')
        login_data = {'email': "jeffa@mail.com", 'password': 'Abcabc123'}
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data.get('token', "")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('articles-api:update_article', kwargs={'slug': self.article1.slug})
        data = {'title': self.article1.title, 'content': 'Content has been updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_article_update_by_non_author(self):
        login_url = reverse('accounts-api:login')
        login_data = {'email': "jeffa@mail.com", 'password': 'Abcabc123'}
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data.get('token', "")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('articles-api:update_article', kwargs={'slug': self.article2.slug})
        data = {'title': self.article2.title, 'content': 'Content has been updated'}
        response = self.client.put(url, data, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(response.data.get('detail'), 'You are not authorized to modify this article.')

