from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', email='test@email.com', password='test')

        self.post = Post.objects.create(
            title='Test blog', body='Body content', author=self.user)

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), 'A sample title')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1')

    def test_post_content(self):
        self.assertEqual(f'{self.user}', 'testuser')
        self.assertEqual(f'{self.post.title}', 'Test blog')
        self.assertEqual(f'{self.post.body}', 'Body content')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test blog')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1')
        no_response = self.client.get('/post/10000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Body content')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New Title',
            'body': 'Something',
            'author': self.user
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Title')
        self.assertContains(response, 'Something')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text'
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)
