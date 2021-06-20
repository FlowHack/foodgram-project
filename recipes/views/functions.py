from django.db.models import Sum
from django.shortcuts import get_object_or_404

import recipes.settings as recipes_settings
from recipes.models import Ingredient, QuantityIngredient


def get_tags(get_params):
    tags = dict(get_params)
    tags.pop('page', tags)

    return list(tags.keys())


def get_recipes_by_tags(get_params, objects):
    tags = get_tags(get_params)

    if not tags:
        return objects.all()

    return objects.filter(
        tag__tag__in=tags
    ).distinct()


def create_quantity_ingredients(data, recipe):
    for item in data:
        QuantityIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=item['ingredient'],
            quantity=item['quantity']
        )


def get_ingredients_and_validate(data):
    ingredients = []

    for item in data.keys():
        if item.startswitch('nameIngredient_'):
            number = item.split('nameIngredient_')[1]
            title = data[item]
            value = data['valueIngredient_' + number]
            units = data['unitsIngredient_' + number]

            if int(value) <= 0:
                raise ValueError(
                    f'Количество ингредиента не может быть = {value}'
                )

            __ingredient = get_object_or_404(
                Ingredient, title=title, dimension=units
            )

            ingredients.append({'ingredient': __ingredient, 'quantity': value})

    if len(ingredients) == 0:
        raise ValueError('Обязательное поле')

    return ingredients


def ingredients_for_download(user):
    unprepared_ingredients = QuantityIngredient.objects.filter(
        recipe__shoplists__user=user
    ).values(
        'ingredient__title', 'ingredient__dimension'
    ).annotate(sum_ingredients=Sum('quantity'))

    return [
        recipes_settings.TEMPLATE_SHOPLIST_RECORD.format(
            title=item['ingredient__title'].capitalize(),
            quantity=item['sum_ingredients'],
            dimension=item['ingredient__dimension']
        )
        for item in unprepared_ingredients
    ]


def get_tags_for_edit(recipe):
    tags = recipe.tag.all().values('tag')

    return [tag['tag'] for tag in tags]
