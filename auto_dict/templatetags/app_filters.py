from django import template
import json
from django.utils.safestring import mark_safe
register = template.Library()

# from ..models import Video


# from django.conf import settings
# try:
#     from django.contrib.auth import get_user_model
#     User = settings.AUTH_USER_MODEL
# except ImportError:
#     from django.contrib.auth.models import User

@register.filter
def to_char(value):
    return chr(96 + value)


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.simple_tag
def is_watched(video_id, user_id):
    """
    Tells if a video is watched
    """
    video = Video.objects.get(pk=video_id)
    if video.is_watched(user_id):
        return 'btn-default'
    else:
        return 'btn-primary'