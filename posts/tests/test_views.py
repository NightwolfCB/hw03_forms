from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post


class YatubeViewTests(TestCase):
    @classmethod
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_user(username='StasBaretskiy')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        group = Group.objects.create(
            title='Test group',
            slug='test_group',
            description='Test description'
        )
        templates_pages_names = {
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),
            'group.html': (
                reverse('group', kwargs={'slug': 'test_group'})
            ),
        }
        
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом"""
        User = get_user_model()
        Post.objects.create(
            text='Тестовый текст',
            author=User.objects.create(username='Тестовый пользователь')
        )
        response = self.authorized_client.get(reverse('index'))
        post_text_0 = response.context.get('posts')[0].text
        post_author_0 = response.context.get('posts')[0].author
        self.assertEqual(post_text_0, 'Тестовый текст', post_text_0)
        self.assertEqual(post_author_0.username, 'Тестовый пользователь', post_author_0)
        
    def test_group_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        group = Group.objects.create(
            title='Test group',
            slug='test_group',
            description='Test description'
        )
        response = self.authorized_client.get(
                reverse('group', kwargs={'slug': 'test_group'})
        )
        self.assertEqual(response.context.get('group').title, 'Test group')
        self.assertEqual(response.context.get('group').description, 'Test description')
        self.assertEqual(response.context.get('group').slug, 'test_group')

    def test_new_post_page_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField
        }        

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_shows_in_index_page(self):
        """Созданный пост с указанной группой появляется на главной странице сайта"""
        User = get_user_model()
        Post.objects.create(
            text='По шоссе',
            author=User.objects.create(username='Саша'),
            group=Group.objects.create(title='Шла')
        )
        response = self.authorized_client.get(reverse('index'))
        post_text_0 = response.context.get('posts')[0].text
        post_author_0 = response.context.get('posts')[0].author
        post_group_0 = response.context.get('posts')[0].group
        self.assertEqual(post_text_0, 'По шоссе', post_text_0)
        self.assertEqual(post_author_0.username, 'Саша', post_author_0)
        self.assertEqual(post_group_0.title, 'Шла', post_group_0)

    def test_post_shows_in_correct_group(self):
        """Созданный пост находится на странице выбранной группы"""
        User = get_user_model()
        post_test = Post.objects.create(
            text='Тестовый текст',
            author=User.objects.create(username='GeorgeMiloslavsky'),
            group=Group.objects.create(title='Test group right')
        )
        group_right = Group.objects.create(
            title='Test group right',
            slug='test_group_right',
            description='Test description 2'
        )
        group_wrong = Group.objects.create(
            title='Test group wrong',
            slug='test_group_wrong',
            description='Test description 3'
        )
        response_1 = self.authorized_client.get(
                reverse('group', kwargs={'slug': 'test_group_right'})
        )
        response_2 = self.authorized_client.get(
                reverse('group', kwargs={'slug': 'test_group_wrong'})
        )
        self.assertEqual(response_1.context.get('group').title, post_test.group.title)
        self.assertNotEqual(response_2.context.get('group').title, post_test.group.title)
