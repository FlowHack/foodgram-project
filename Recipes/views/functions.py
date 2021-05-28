from Recipes.models import Recipe


def get_recipes_by_tags(get_params):
    if (len(get_params) == 0) or (
            len(get_params) == 1 and get_params.get('page')):
        return Recipe.objects.all()

    return Recipe.objects.filter(
        tag__tag__in=list(get_params.keys())
    ).distinct()
