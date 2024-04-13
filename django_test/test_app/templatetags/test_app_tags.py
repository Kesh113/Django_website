from django import template
import test_app.views as views
from django.db.models import Count
from test_app.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('test_app/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('test_app/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}