from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})

@register.filter(name='duration_format')
def duration_format(duration):
    if isinstance(duration, timedelta):
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours}h {minutes}m"
    return duration  # Return the original value if it's not a timedelta