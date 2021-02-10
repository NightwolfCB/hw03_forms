from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User


class YatubePaginatorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        number_of_posts = 228
        cls.user = User.objects.create(username='GladiatorPWNZ')
        for post_num in range(number_of_posts):
            Post.objects.create(
                text='да да я '*post_num,
                author=cls.user,
                group=Group.objects.create(title='Да я да я')
            )

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_containse_ten_records(self):
        """На первой странице ровно 10 постов"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_twenty_third_page_containse_eight_records(self):
        """На двадцать третьей странице ровно 8 постов"""
        response = self.client.get(reverse('index') + '?page=23')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('page').object_list), 8)
