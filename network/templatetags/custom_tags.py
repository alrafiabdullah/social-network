from django import template
from ..models import Comment

register = template.Library()


@register.simple_tag
def comm(id):
    comment_list = []
    comment_obj = Comment.objects.filter(of_post_id=id)
    for come in comment_obj:
        comment_list.append(come)

    return comment_list
