from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Group

class YatubeURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='Test group',
            slug='test_group',
            description='Test description'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(username='StasBaretskiy')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_home_url_exists_at_desired_location(self):
        """Главная страница доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_added_url_exists_at_desired_location(self):
        """Страница группы /group/test_group/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test_group/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_exists_at_desired_location(self):
        """Страница создания нового поста /new/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_redirect_anonymous(self):
        """Страница по адресу /new/ перенаправляет неавторизированного пользователя."""
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'index.html': '/',
            'group.html': '/group/test_group/',
            'new.html': '/new/'
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
