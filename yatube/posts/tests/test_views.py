import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Comment, Group, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ViewsTest(TestCase):
    """Класс для тестирования view-функции."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='bimo')
        cls.user_jake = User.objects.create_user(username='jake')
        cls.image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='test-image.png',
            content=cls.image,
            content_type='image'
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
            image=uploaded
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый комментарий'
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
        cls.post_comments_url = reverse(
            'posts:add_comment',
            kwargs={'post_id': f'{cls.post.id}'}
        )
        cls.follow_index_url = reverse('posts:follow_index')
        cls.profile_follow_url = reverse(
            'posts:profile_follow',
            kwargs={'username': f'{cls.user_jake.username}'}
        )
        cls.profile_unfollow_url = reverse(
            'posts:profile_unfollow',
            kwargs={'username': f'{cls.user_jake.username}'}
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_templates(self):
        """Проверка на соответствие шаблонов и namespases."""
        page_name_templates = (
            (self.index_url, 'posts/index.html'),
            (self.post_create_url, 'posts/post_create.html'),
            (self.group_list_url, 'posts/group_list.html'),
            (self.profile_url, 'posts/profile.html'),
            (self.post_detail_url, 'posts/post_detail.html'),
            (self.post_edit_url, 'posts/post_create.html'),
            (self.follow_index_url, 'posts/follow.html'),
        )
        for reverse_name, template in page_name_templates:
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(self.index_url)
        context = response.context['page_obj'].object_list[0]
        self.assertEqual(context.text, self.post.text)
        self.assertEqual(context.author, self.post.author)
        self.assertEqual(context.group, self.post.group)
        self.assertEqual(context.image, self.post.image)

    def test_group_list_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(self.group_list_url)
        context = response.context['page_obj'].object_list[0]
        self.assertEqual(context.text, self.post.text)
        self.assertEqual(context.author, self.post.author)
        self.assertEqual(context.group, self.post.group)
        self.assertEqual(context.image, self.post.image)
        self.assertEqual(context.group.slug, self.group.slug)
        self.assertEqual(context.group.title, self.group.title)
        self.assertEqual(context.group.description, self.group.description)

    def test_profile_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.profile_url)
        context = response.context['page_obj'].object_list[0]
        self.assertEqual(context.group, self.post.group)
        self.assertEqual(context.text, self.post.text)
        self.assertEqual(context.image, self.post.image)
        self.assertEqual(response.context['count_posts'], Post.objects.count())
        self.assertEqual(response.context['author'], self.post.author)

    def test_post_detail_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.guest_client.get(self.post_detail_url)
        selected_post = response.context['selected_post']
        self.assertEqual(selected_post.id, self.post.id)
        self.assertEqual(selected_post.image, self.post.image)
        self.assertEqual(response.context['count_posts'], Post.objects.count())

    def test_create_post_context(self):
        """Шаблон create_post для создание поста
        сформирован с правильным контекстом.
        """
        response = self.authorized_client.get(self.post_create_url)
        form = response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_edit_post_context(self):
        """Шаблон edit_post для редактирования поста
        сформирован с правильным контекстом.
        """
        response = self.authorized_client.get(self.post_edit_url)
        is_edit = response.context['is_edit']
        form = response.context['form']
        self.assertTrue(is_edit, True)
        self.assertIsInstance(form, PostForm)

    def test_group_post_in_index(self):
        """Проверка, что у поста есть группа на странице index."""
        response = self.guest_client.get(self.index_url)
        group = response.context['page_obj'].object_list[0].group
        self.assertEqual(group, self.post.group)
        self.assertEqual(group, self.group)

    def test_group_post_in_group_list(self):
        """Проверка, что у поста есть группа на странице group_list."""
        response = self.guest_client.get(self.group_list_url)
        group = response.context['page_obj'].object_list[0].group
        self.assertEqual(group, self.post.group)
        self.assertEqual(group, self.group)

    def test_group_post_in_profile(self):
        """Проверка, что у поста есть группа на странице profile."""
        response = self.authorized_client.get(self.profile_url)
        group = response.context['page_obj'].object_list[0].group
        self.assertEqual(group, self.post.group)
        self.assertEqual(group, self.group)

    def test_comments_only_for_authorized_client(self):
        """Проверка, что комментарии может оставлять
        только авторизованный пользователь.
        """
        response = self.guest_client.get(self.post_comments_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_detail_comments(self):
        """Проверка, что комментарий появляется на странице post_detail."""
        response = self.authorized_client.get(self.post_detail_url)
        comment = response.context['selected_post'].comments.filter(pk=1)[0]
        self.assertEqual(comment, self.comment)

    def test_cache_index_page(self):
        """Проверка кэша на posts:index."""
        response = self.guest_client.get(self.index_url)
        Post.objects.create(
            author=self.user,
            text='Пост не в кэше',
        )
        new_response = self.guest_client.get(self.index_url)
        post_text = response.context['page_obj'].object_list[0].text
        new_post_text = new_response.context['page_obj'].object_list[0].text
        self.assertNotEqual(post_text, new_post_text)

    def test_follow_index_only_for_authorized_client(self):
        """Проверка, что на страницу подписок попадает
        только авторизованный пользователь.
        """
        response = self.guest_client.get(self.follow_index_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_profile_follow(self):
        """Проверка, что юзер подписался."""
        response = self.authorized_client.get(self.profile_follow_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.follow_index_url)

    def test_follow_index_context(self):
        """Шаблон follow.html сформирован с правильным контекст."""
        cache.clear()
        self.authorized_client.get(self.profile_follow_url)
        jake_post = Post.objects.create(
            author=self.user_jake,
            text='Тестовый пост user_jake',
        )
        response = self.authorized_client.get(self.follow_index_url)
        context = response.context['page_obj'].object_list[0]
        self.assertEqual(context.text, jake_post.text)
        self.assertEqual(context.author, jake_post.author)

    def test_profile_unfollow(self):
        """Проверка, что юзер отписался."""
        response = self.authorized_client.get(self.profile_unfollow_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.follow_index_url)
