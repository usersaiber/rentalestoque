from django import template

register = template.Library()

@register.filter(name='getattr')
def getattr_filter(obj, attr):
    """
    Retorna o valor de um atributo de um objeto.
    """
    try:
        return getattr(obj, attr, None)
    except AttributeError:
        return None
