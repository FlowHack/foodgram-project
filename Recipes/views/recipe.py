from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render

from Recipes import settings as recipes_settings
from Recipes.models import ShoppingList
from Recipes.views import functions

User = get_user_model()


def index(request):
    data_get = request.GET
    recipes = functions.get_recipes_by_tags(data_get)
    count_purchases = (
        0, ShoppingList.objects.filter(user=request.user).count()
    )[request.user.is_authenticated]

    paginator = Paginator(
        recipes, recipes_settings.ITEM_RECIPES_INDEX
    )
    page_number = data_get.get('page')
    page = paginator.get_page(page_number)

    context = {
        'recipes': recipes,
        'count_purchases': count_purchases,
        'paginator': paginator,
        'page': page
    }
    return render(request, 'recipe/index.html', context=context)


def author_page(request):
    pass


def recipe(request):
    pass


def new_recipe(request):
    pass


def edit_recipe(request):
    pass


def follows_page(request):
    pass


def favorite_recipes(request):
    pass


def shop_list_page(request):
    pass
