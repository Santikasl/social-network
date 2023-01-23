from django import template

register = template.Library()


@register.filter(name='color')
def color(post, user):
    return user in post.liked.all()


@register.filter(name='count')
def color(follow):
    return follow.count()

