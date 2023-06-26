from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Фильтр для добавления CSS-класса в шаблон."""
    return field.as_widget(attrs={'class': css})
