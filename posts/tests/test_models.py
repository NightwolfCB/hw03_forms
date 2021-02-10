from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Group, Post


class YatubeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create()
        Post.objects.create(
            text='Тестовый текст',
            author=cls.user
        )
        cls.post = Post.objects.get()
        Group.objects.create(
            id=1,
            title='A'*200,
            slug='test_group',
            description='Б'*200
        )
        cls.group = Group.objects.get(slug='test_group')

    def test_post_verbose_name(self):
        """verbose_name в полях Post совпадает с ожидаемым."""
        post = YatubeModelTest.post
        field_verboses = {
            'text': 'Текст публикации',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Сообщество',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_post_help_text(self):
        """help_text в полях Post совпадает с ожидаемым."""
        post = YatubeModelTest.post
        field_help_texts = {
            'text': 'Напишите текст вашей публикации',
            'author': 'Ваше имя',
            'group': 'Выберите группу'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_post_content_is_text_field(self):
        """__str__  post - это строчка с содержимым post.text."""
        post = YatubeModelTest.post
        expected_post_content = post.text[:15]
        self.assertEquals(expected_post_content, str(post))

    def test_group_verbose_name(self):
        """verbose_name в полях Group совпадает с ожидаемым."""
        group = YatubeModelTest.group
        field_verboses = {
            'title': 'Название',
            'slug': 'Слаг',
            'description': 'Описание'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_group_help_text(self):
        """help_text в полях Group совпадает с ожидаемым."""
        group = YatubeModelTest.group
        field_help_texts = {
            'title': 'Название вашего сообщества',
            'slug': 'Укажите адрес для вашего сообщества. Используйте '
                     'только латиницу, цифры, дефисы и знаки '
                     'подчёркивания',
            'description': 'Краткое описание вашего сообщества'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_group_title_is_text_field(self):
        """__str__  group - это строчка с содержимым group.title."""
        group = YatubeModelTest.group
        expected_group_content = group.title
        self.assertEquals(expected_group_content, str(group))
