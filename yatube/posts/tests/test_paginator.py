from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()

POSTS_FIRST_PAGE = 10
POSTS_SECOND_PAGE = 4


class PaginatorViewsTest(TestCase):
    """Проверка работы пажинатора."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='pagi')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        for i in range(14):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Тестовый пост {i}',
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()

    def test_index_firts_page_paginator(self):
        """Пажинатор на первой index странице работает корректно."""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), POSTS_FIRST_PAGE)

    def test_index_second_page_paginator(self):
        """Пажинатор на второй index странице работает корректно."""
        response = self.guest_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), POSTS_SECOND_PAGE)

    def test_group_list_firts_page_paginator(self):
        """Пажинатор на первой group_list странице работает корректно."""
        response = self.guest_client.get(reverse(
            'posts:group_list', kwargs={'slug': f'{self.group.slug}'}
        ))
        self.assertEqual(len(response.context['page_obj']), POSTS_FIRST_PAGE)

    def test_group_list_second_page_paginator(self):
        """Пажинатор на второй group_list странице работает корректно."""
        response = self.guest_client.get(reverse(
            'posts:group_list', kwargs={'slug': f'{self.group.slug}'})
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), POSTS_SECOND_PAGE)

    def test_profile_firts_page_paginator(self):
        """Пажинатор на первой profile странице работает корректно."""
        response = self.guest_client.get(reverse(
            'posts:profile', kwargs={'username': f'{self.user.username}'}
        ))
        self.assertEqual(len(response.context['page_obj']), POSTS_FIRST_PAGE)

    def test_profile_second_page_paginator(self):
        """Пажинатор на второй profile странице работает корректно."""
        response = self.guest_client.get(reverse(
            'posts:profile', kwargs={'username': f'{self.user.username}'})
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), POSTS_SECOND_PAGE)
