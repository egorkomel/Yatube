from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        group_str = f'Группа {group.title}'
        self.assertEqual(group_str, str(group))

        post = PostModelTest.post
        post_str = post.text
        self.assertEqual(post_str, str(post))

    def test_verbose_name(self):
        """Проверяем verbose_name у моделей."""
        post = PostModelTest.post
        field_verbose = (
            ('author', 'Автор'),
            ('group', 'Группа')
        )

        for field, expected_value in field_verbose:
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text(self):
        """Проверяем help_text у моделей."""
        post = PostModelTest.post
        field_help_text = (
            ('text', 'Введите текст поста'),
            ('group', 'Группа, к которой будет относиться пост'),
        )

        for field, expected_value in field_help_text:
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
