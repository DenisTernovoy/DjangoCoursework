from django import template

register = template.Library()


@register.filter()
def show_product_photo(path):
    if path:
        return f"/media/{path}"
    else:
        return "#"
