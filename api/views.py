from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

import api.settings as api_settings
from recipes.models import Favorite, Ingredient, Recipe, ShoppingList
from users.models import Follow

User = get_user_model()


@api_view(['POST', 'DELETE'])
def purchases(request):
    recipe_id = request.data.get('id')

    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shop_list, result = ShoppingList.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if not result:
            raise api_settings.RESPONSE_400_EXIST

        return api_settings.RESPONSE_SUCCESS

    if request.method == 'DELETE':
        result = ShoppingList.objects.filter(
            recipe__id=recipe_id
        ).delete()[0]
        if not result:
            return api_settings.RESPONSE_400_NOT_EXISTS

        return api_settings.RESPONSE_SUCCESS

    return api_settings.RESPONSE_400


@api_view(['POST', 'DELETE'])
def favorites(request):
    recipe_id = request.data.get('id')

    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite, result = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if not result:
            return api_settings.RESPONSE_400_EXIST

        return api_settings.RESPONSE_SUCCESS

    if request.method == 'DELETE':
        result = Favorite.objects.filter(
            recipe__id=recipe_id
        ).delete()
        if not result:
            return api_settings.RESPONSE_400_NOT_EXISTS

        return api_settings.RESPONSE_SUCCESS

    return api_settings.RESPONSE_400


@api_view(['POST', 'DELETE'])
def follow(request):
    author_id = request.data.get('id')
    if not User.objects.filter(id=author_id).exists():
        return api_settings.RESPONSE_404_NOT_AUTHOR

    if request.method == 'POST':
        if request.user.id == author_id:
            return api_settings.RESPONSE_400_CANT_SUBSCRIBE_YOURSELF

        author = get_object_or_404(User, id=author_id)
        follow, result = Follow.objects.get_or_create(
            user=request.user,
            author=author
        )
        if not result:
            return api_settings.RESPONSE_400_EXIST

        return api_settings.RESPONSE_SUCCESS

    if request.method == 'DELETE':
        result = Follow.objects.filter(
            user=request.user,
            author__id=author_id
        ).delete()
        if not result:
            return api_settings.RESPONSE_400_NOT_EXISTS

        return api_settings.RESPONSE_SUCCESS

    return api_settings.RESPONSE_400


@api_view(['GET'])
def ingredients(request):
    query = request.GET.get('query')

    ingredients = list(Ingredient.objects.filter(
        title__icontains=query
    ).values('title', 'dimension'))

    return Response(ingredients)
