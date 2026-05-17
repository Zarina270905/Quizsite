from django import template
from quizzes.models import Category, Tag

register = template.Library()

@register.simple_tag
def get_categories():
    cats = Category.objects.all()
    return [cat.name for cat in cats]

@register.simple_tag
def popular_tests(limit=3):
    tests = [
        {'id': 1, 'title': 'Основы Python', 'views': 150},
        {'id': 2, 'title': 'HTML и CSS', 'views': 120},
        {'id': 3, 'title': 'Базы данных SQL', 'views': 95},
    ]
    return tests[:limit]

@register.inclusion_tag('quizzes/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected}

@register.inclusion_tag('quizzes/popular.html')
def show_popular(limit=3):
    tests = popular_tests(limit)
    return {'popular_tests': tests}

@register.inclusion_tag('quizzes/list_tags.html')
def show_all_tags():
    tags = Tag.objects.all()
    return {'tags': tags}