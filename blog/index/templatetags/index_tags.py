from django import template
from blog_index.models import BlogModel
register = template.Library()


@register.simple_tag
def get_blog_title(obj_id):
    return BlogModel.objects.get(id=obj_id).title



