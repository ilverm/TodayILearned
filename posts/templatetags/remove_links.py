from django import template

from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def remove_links(value):
    """
    Extracts the text content from an HTML link (<a> tag)
    in the given HTML string.
    """

    try:
        soup = BeautifulSoup(value, 'html.parser')
        link = soup.find('a')
        if link:
            link.replace_with(link.text)
            value = str(soup)
    except Exception as e:
        # Is there a more specific exception?
        print(f"An error occurred: {e}")

    return value