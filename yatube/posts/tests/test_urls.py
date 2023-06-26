from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    """Класс для тестирования статических URL."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='human_fin')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.index_url = reverse('posts:index')
        cls.post_create_url = reverse('posts:post_create')
        cls.group_list_url = reverse(
            'posts:group_list',
            kwargs={'slug': f'{cls.group.slug}'}
        )
        cls.profile_url = reverse(
            'posts:profile',
            kwargs={'username': f'{cls.user.username}'}
        )
        cls.post_detail_url = reverse(
            'posts:post_detail',
            kwargs={'post_id': f'{cls.post.id}'}
        )
        cls.post_edit_url = reverse(
            'posts:post_edit',
            kwargs={'post_id': f'{cls.post.id}'}
        )
        cls.follow_index_url = reverse('posts:follow_index')
        cls.profile_follow_url = reverse(
            'posts:profile_follow',
            kwargs={'username': f'{cls.user.username}'}
        )
        cls.profile_unfollow_url = reverse(
            'posts:profile_unfollow',
            kwargs={'username': f'{cls.user.username}'}
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_public_urls(self):
        """Проверка общедоступных страниц."""
        urls = (
            self.index_url,
            self.group_list_url,
            self.profile_url,
            self.post_edit_url,
            self.follow_index_url,
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page(self):
        """Проверка ответа на несуществующую страницу."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_edit_post(self):
        """Проверка редактирования поста."""
        self.authorized_client = Client()
        self.authorized_client.force_login(user=self.post.author)
        response = self.authorized_client.get(self.post_edit_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_post(self):
        """Проверка создания поста."""
        response = self.authorized_client.get(self.post_create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_follow(self):
        """Проверка, что при переходе на posts:profile_follow
        происходит переадресация.
        """
        response = self.authorized_client.get(self.profile_follow_url)
        self.assertRedirects(response, self.follow_index_url)

    def test_profile_unfollow(self):
        """Проверка, что при переходе на posts:profile_unfollow
        происходит переадресация.
        """
        response = self.authorized_client.get(self.profile_unfollow_url)
        self.assertRedirects(response, self.follow_index_url)

    def test_template(self):
        """Проверка URL и шаблонов."""
        urls_templates = (
            (self.index_url, 'posts/index.html'),
            (self.group_list_url, 'posts/group_list.html'),
            (self.profile_url, 'posts/profile.html'),
            (self.post_detail_url, 'posts/post_detail.html'),
            (self.post_edit_url, 'posts/post_create.html'),
            (self.post_create_url, 'posts/post_create.html'),
            (self.follow_index_url, 'posts/follow.html')
        )

        for url, template in urls_templates:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
