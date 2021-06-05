from django.forms.utils import ErrorList

from Recipes.models import Ingredient, QuantityIngredient, Recipe, Tag


def get_recipes_by_tag(get_params, **kwargs):
    favorite = kwargs.get('favorite')
    user = kwargs.get('user')

    if (len(get_params) == 0) or (
            len(get_params) == 1 and get_params.get('page')):
        if favorite is not None:
            return Recipe.favorites_by_user(user)
        if user is not None:
            return user.recipes.all()
        return Recipe.objects.all()

    if favorite is not None:
        return Recipe.favorites_by_user.filter(
            tag__tag__in=list(tag__tag__int=get_params.keys())
        ).distinct()
    if user is not None:
        user.recipes.filter(
            tag__tag__in=list(get_params.keys())
        ).distinct()
    return Recipe.objects.filter(
        tag__tag__in=list(get_params.keys())
    ).distinct()


def get_ingredients_and_validate(data, form):
    ingredients = []
    errors = False

    for item in data.keys():
        if 'nameIngredient_' in item:
            number = item.split('nameIngredient_')[1]
            title = data[item]
            value = data['valueIngredient_' + number]
            units = data['unitsIngredient_' + number]

            if int(value) <= 0:
                form._errors['ingredients'] = ErrorList(
                    [f'Количество ингредиента не может быть = {value}']
                )
                errors = True
                continue
            try:
                __ingredient = Ingredient.objects.get(
                    title=title, dimension=units
                )
            except Ingredient.DoesNotExist:
                form._errors['ingredients'] = ErrorList(
                    [f'Не существует ингредиента: {title}']
                )
                errors = True
                continue

            ingredient = QuantityIngredient.objects.create(
                ingredient=__ingredient,
                quantity=value
            )
            ingredients.append(ingredient)

    if len(ingredients) == 0:
        errors = True
        form._errors['ingredients'] = ErrorList(['Обязательное поле'])

    if errors is True:
        return {'form': form}

    return {'ingredients': ingredients}


def get_tags_and_validate(data, form):
    tags = []
    errors = False

    try:
        if 'dinner' in data.keys():
            tags.append(Tag.objects.get(tag='dinner'))
        if 'breakfast' in data.keys():
            tags.append(Tag.objects.get(tag='breakfast'))
        if 'lunch' in data.keys():
            tags.append(Tag.objects.get(tag='lunch'))
    except Tag.DoesNotExist:
        errors = True
        form._errors['tags'] = ErrorList(
            ['В BD нет такой записи, обратитесь к администратору']
        )

    if len(tags) == 0:
        errors = True
        form._errors['tags'] = ErrorList(['Обязательное поле'])
    if errors is True:
        return {'form': form}

    return {'tags': tags}


def ingredients_for_download(unprepared_ingredients):
    ingredients = {}

    for ingredient in unprepared_ingredients:
        title = ingredient['ingredients__ingredient__title']
        dimension = ingredient['ingredients__ingredient__dimension']
        quantity = ingredient['ingredients__quantity']

        if title in ingredients:
            ingredients[title][1] += quantity
            continue

        ingredients[title] = [title, quantity, dimension]

    ingredients = list(ingredients.values())
    for i in range(len(ingredients)):
        item = ingredients[i]
        ingredients[i] = f'{item[0].capitalize()} - {item[1]}{item[2]}'

    txt_ingredients = '\n'.join(ingredients)

    return txt_ingredients


def get_ingredients_for_edit(recipe):
    __ingredients = recipe.ingredients.all().values(
        'ingredient__title',
        'ingredient__dimension',
        'quantity'
    )
    ingredients = []

    for i in range(len(__ingredients)):
        ingredient = __ingredients[i]
        ing_id = i + 1
        title = ingredient['ingredient__title']
        dimension = ingredient['ingredient__dimension']
        quantity = ingredient['quantity']

        ingredients.append(
            {
                'ing_id': f'ing_{ing_id}',
                'name': {
                    'name': f'nameIngredient_{ing_id}',
                    'value': title
                },
                'value': {
                    'name': f'valueIngredient_{ing_id}',
                    'value': quantity
                },
                'units': {
                    'name': f'unitsIngredient_{ing_id}',
                    'value': dimension
                }
            }
        )

    return ingredients


def get_tags_for_edit(recipe):
    tags = recipe.tag.all().values('tag')
    tags = [tag['tag'] for tag in tags]

    return tags
