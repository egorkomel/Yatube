from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """View-класс для рендера страницы автора сайта."""

    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """View-класс для рендера страницы используемого стека."""

    template_name = 'about/tech.html'
