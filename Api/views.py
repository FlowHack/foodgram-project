from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Recipes.models import Favorite, Ingredient, Recipe, ShoppingList
from Users.models import Follow

User = get_user_model()


@api_view(['POST', 'DELETE'])
def purchases(request):
    recipe_id = request.data.get('id') or request.GET.get('id')
    print(recipe_id)

    if request.method == 'POST':
        try:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            result = ShoppingList.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if result[1] is False:
                raise ValueError('Такой объект уже имеется')

            return Response({'success': 'true'})
        except Exception as error:
            return Response(
                {'success': 'false', 'error': str(error)},
                status=status.HTTP_404_NOT_FOUND
            )

    if request.method == 'DELETE':
        try:
            ShoppingList.objects.filter(
                recipe__id=recipe_id
            ).delete()
            return Response({'success': 'true'})
        except Exception as error:
            print(str(error))
            return Response(
                {'success': 'false', 'error': str(error)},
                status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {'success': 'false'}, status=status.HTTP_404_NOT_FOUND
    )


@api_view(['POST', 'DELETE'])
def favorites(request):
    recipe_id = request.data.get('id') or request.GET.get('id')

    if request.method == 'POST':
        try:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            result = Favorite.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if result[1] is False:
                raise ValueError('Такой объект уже имеется')

            return Response({'success': 'true'})
        except Exception as error:
            return Response(
                {'success': 'false', 'error': str(error)},
                status=status.HTTP_404_NOT_FOUND
            )

    if request.method == 'DELETE':
        try:
            Favorite.objects.filter(
                recipe__id=recipe_id
            ).delete()
            return Response({'success': 'true'})
        except Exception as error:
            return Response(
                {'success': 'false', 'error': str(error)},
                status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {'success': 'false'}, status=status.HTTP_404_NOT_FOUND
    )


@api_view(['POST', 'DELETE'])
def follow(request):
    author_id = request.data.get('id') or request.GET.get('id')

    if request.method == 'POST':
        try:
            if request.user.id == author_id:
                raise ValueError('Нельзя подписаться на себя')

            author = get_object_or_404(User, id=author_id)
            result = Follow.objects.get_or_create(
                user=request.user,
                author=author
            )
            if result[1] is False:
                raise ValueError('Такой объект уже имеется')

            return Response({'success': 'true'})
        except Exception as error:
            return Response(
                {'success': 'false', 'error': str(error)},
                status=status.HTTP_404_NOT_FOUND
            )

    if request.method == 'DELETE':
        try:
            Follow.objects.filter(
                user=request.user,
                author__id=author_id
            ).delete()
            return Response({'success': 'true'})
        except Exception as error:
            return Response(
                {'success': 'false', 'error': str(error)},
                status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {'success': 'false'}, status=status.HTTP_404_NOT_FOUND
    )


@api_view(['GET'])
def ingredients(request):
    query = request.GET.get('query')

    ingredients = list(Ingredient.objects.filter(
        title__icontains=query
    ).values('title', 'dimension'))

    return Response(ingredients)
