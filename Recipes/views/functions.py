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
