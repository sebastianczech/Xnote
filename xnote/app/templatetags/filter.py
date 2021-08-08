from datetime import datetime, timedelta

from django import template
from django.utils import dateparse
from monthdelta import monthdelta

register = template.Library()


@register.filter(name='input_type')
def input_type(field):
    return field.field.widget.__class__.__name__


@register.filter(name='add_class')
def add_class(field, given_class):
    existing_classes = field.field.widget.attrs.get('class', None)
    if existing_classes:
        if existing_classes.find(given_class) == -1:
            classes = existing_classes + ' ' + given_class
        else:
            classes = existing_classes
    else:
        classes = given_class
    return field.as_widget(attrs={"class": classes})


@register.filter(name='calculate_date_for_reminder_with_repeat')
def calculate_date_for_reminder_with_repeat(reminder, repeat):
    present_datetime = datetime.now()
    reminder_datetime = datetime.strptime(reminder, '%Y-%m-%d %H:%M')
    if present_datetime > reminder_datetime:
        while present_datetime > reminder_datetime:
            if repeat == '1d':
                reminder_datetime = reminder_datetime + timedelta(days=1)
            elif repeat == '7d':
                reminder_datetime = reminder_datetime + timedelta(days=7)
            elif repeat == '14d':
                reminder_datetime = reminder_datetime + timedelta(days=14)
            elif repeat == '30d':
                reminder_datetime = reminder_datetime + timedelta(days=30)
            elif repeat == '1m':
                reminder_datetime = reminder_datetime + monthdelta(1)
            elif repeat == '2m':
                reminder_datetime = reminder_datetime + monthdelta(2)
            elif repeat == '3m':
                reminder_datetime = reminder_datetime + monthdelta(3)
            elif repeat == '1y':
                reminder_datetime = reminder_datetime + monthdelta(12)
            else:
                break
        return reminder_datetime.strftime("%Y-%m-%d %H:%M")
    else:
        return reminder


@register.filter(name='datetime_iso_8601_to_datetime')
def datetime_iso_8601_to_datetime(value):
    return dateparse.parse_datetime(value)
