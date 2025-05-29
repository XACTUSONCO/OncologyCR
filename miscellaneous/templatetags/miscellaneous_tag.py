from django import template

register = template.Library()


@register.filter
@register.simple_tag
def get_week_day_from_datetime(dt):
    if dt is None:
        return ""
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    return weekdays[dt.weekday()]
