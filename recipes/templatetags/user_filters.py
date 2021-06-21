from django import template
from django.shortcuts import get_object_or_404

import recipes.settings as recipes_settings

register = template.Library()


@register.filter
def in_follower(user, author):
    return author.following.filter(user=user).exists()


@register.filter
def in_shoplist(recipe, user):
    return user.shoplists.filter(recipe=recipe).exists()


@register.filter
def in_favorite(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()


@register.filter
def addclass(field, css):
    css = css.split('&')
    if len(css) == 2:
        return field.as_widget(attrs={'class': css[0], 'style': css[1]})

    return field.as_widget(attrs={'class': css[0]})


@register.filter
def ingredient_quantity(ingredient, recipe):
    return get_object_or_404(
        ingredient.quantity_ingredients, recipe=recipe
    ).quantity


@register.filter
def pluralize_recipe(value):
    variants = recipes_settings.RECIPE_VARIANTS

    if value % 100 == 2 or (value % 100 > 20 and value % 10 == 1):
        return variants[0]
    elif value % 100 == 2 or (value % 100 > 20 and value % 10 == 2):
        return variants[1]
    elif value % 100 == 3 or (value % 100 > 20 and value % 10 == 3):
        return variants[1]
    elif value % 100 == 4 or (value % 100 > 20 and value % 10 == 4):
        return variants[1]

    return variants[2]
