from django.core.paginator import Paginator


def make_paginator(request, posts, max_posts):
    """Util-функция для создания пагинатора."""
    paginator = Paginator(posts, max_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
