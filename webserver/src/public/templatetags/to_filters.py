""" Custom filters for use by templates. Include them using load"""

from django import template
from django.template.defaulttags import register

register = template.Library()                           # pylint: disable=invalid-name

@register.filter
def get_item(dictionary, key):
    """ Allow the template to access dict items based off key variables.
        Use like:
            {{ mydict|get_item:item.NAME }}
    """
    return dictionary.get(key)
