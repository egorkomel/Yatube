from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма для создания нового поста."""

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['group'].empty_label = '--- Выберите группу ---'

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Текст поста отсутствует!')
        return data


class CommentForm(forms.ModelForm):
    """Модель для созданиея нового комментария."""

    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Текст комментария отсутствует!')
        return data
