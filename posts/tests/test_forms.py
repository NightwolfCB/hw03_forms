from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post, User


class YatubeFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='StasBaretskiy')
        cls.group = Group.objects.create(
            title='Test group',
            slug='test_group',
            description='Test description')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_new_post(self):
        """Валидная форма создает запись в Post"""
        posts_count = Post.objects.count()
        form_data = {
            'group': YatubeFormTests.group.id,
            'text': 'Старые навыки не пропадают, понимаешь.'
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(group=YatubeFormTests.group.id).exists())
        self.assertEqual(response.status_code, 200)
