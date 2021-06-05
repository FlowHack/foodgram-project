from django import template

register = template.Library()


@register.filter
def subtraction(value, arg):
    return int(value) + int(arg)


@register.filter
def in_follower(user, author):
    return author.following.filter(user=user).exists()


@register.filter
def in_shoplist(recipe, user):
    return user.shoplists.filter(recipe=recipe)


@register.filter
def in_favorite(recipe, user):
    return user.favorites.filter(recipe=recipe)


@register.filter
def addclass(field, css):
    css = css.split('&')
    if len(css) == 2:
        return field.as_widget(attrs={'class': css[0], 'style': css[1]})

    return field.as_widget(attrs={'class': css[0]})
