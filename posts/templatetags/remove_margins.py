from django import template

from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def remove_margins(value):
    """
    Remove bottom margin from an HTML paragraph (<p> tag)
    """

    try:
        soup = BeautifulSoup(value, 'html.parser')
        for paragraph in soup.find_all('p'):
            paragraph.unwrap()
        value = str(soup)
    except Exception as e:
        pass

    return value