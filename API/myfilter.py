from django.template import Library
import markdown
register=Library()

def md(value):
    return markdown.markdown(value)