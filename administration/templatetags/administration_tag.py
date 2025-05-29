from django import template
from administration.models import Organization

register = template.Library()


@register.filter
@register.simple_tag
def get_week_day_from_datetime(dt):
    if dt is None:
        return ""
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    return weekdays[dt.weekday()]



@register.filter
@register.simple_tag
def get_date_format(dt):
    if dt is None:
        return ""
    return dt.strftime("%Y-%m-%d")


@register.simple_tag
def get_organization():
    organizations = Organization.objects.filter(is_deleted=0)
    return organizations
