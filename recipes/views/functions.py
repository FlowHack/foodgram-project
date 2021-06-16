from collections import defaultdict

from recipes.models import Ingredient, QuantityIngredient, Recipe, Tag


def get_tags(get_params):
    if 'page' in get_params:
        del(get_params['page'])

    return list(get_params.keys())


def get_recipes_by_tags(get_params, objects):
    tags = get_tags(get_params)

    if len(tags) == 0:
        return objects.all()

    return objects.filter(
        tag__tag__in=tags
    ).distinct()


def create_quantity_ingredients(data, recipe):
    for item in data:
        QuantityIngredient.objects.create(
            recipe=recipe,
            ingredient=item['ingredient'],
            quantity=item['quantity']
        )


def get_ingredients_and_validate(data):
    ingredients = []

    for item in data.keys():
        if 'nameIngredient_' in item:
            number = item.split('nameIngredient_')[1]
            title = data[item]
            value = data['valueIngredient_' + number]
            units = data['unitsIngredient_' + number]

            if int(value) <= 0:
                raise ValueError(
                    f'Количество ингредиента не может быть = {value}'
                )

            try:
                __ingredient = Ingredient.objects.get(
                    title=title, dimension=units
                )
            except Ingredient.DoesNotExist:
                raise ValueError(f'Не существует ингредиента: {title}')

            ingredients.append({'ingredient': __ingredient, 'quantity': value})

    if len(ingredients) == 0:
        raise ValueError('Обязательное поле')

    return ingredients


def get_tags_and_validate(data):
    all_tags = Tag.objects.all().values_list('tag')
    tags = []

    try:
        for item in data.keys():
            if (item, ) in all_tags:
                tags.append(Tag.objects.get(tag=item))
    except Tag.DoesNotExist:
        raise ValueError('В BD нет такого тега')

    if len(tags) == 0:
        raise ValueError('Обязательное поле')

    return tags


def ingredients_for_download(user):
    ingredients = defaultdict(lambda: ['', 0, ''])
    unprepared_ingredients = Recipe.objects.filter(
        shoplists__user=user
    ).values(
        'ingredients__title',
        'ingredients__dimension',
        'quantity_ingredients__quantity'
    )

    for ingredient in unprepared_ingredients:
        title = ingredient['ingredients__title']
        dimension = ingredient['ingredients__dimension']
        quantity = ingredient['quantity_ingredients__quantity']

        quantity += ingredients[title][1]
        ingredients[title] = [title, quantity, dimension]

    for key, value in ingredients.items():
        ingredients[key] = f'{value[0].capitalize()} - {value[1]}{value[2]}'

    return ingredients.values()


def get_tags_for_edit(recipe):
    tags = recipe.tag.all().values('tag')

    return [tag['tag'] for tag in tags]
