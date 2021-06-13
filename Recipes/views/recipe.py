from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from Recipes import settings as recipes_settings
from Recipes.forms import RecipeForm
from Recipes.models import Recipe
from Recipes.views import functions

User = get_user_model()


def index(request):
    data_get = request.GET

    recipes = functions.get_recipes_by_tag(data_get)

    paginator = Paginator(
        recipes, recipes_settings.ITEM_RECIPES_INDEX
    )
    page_number = data_get.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'index': True
    }
    return render(request, 'recipe/index.html', context=context)


def author_page(request, username):
    data_get = request.GET
    author = get_object_or_404(User, username=username)
    recipes = functions.get_recipes_by_tag(data_get, user=author)

    paginator = Paginator(
        recipes, recipes_settings.ITEM_RECIPES_AUTHOR_PAGE
    )
    page_number = data_get.get('page')
    page = paginator.get_page(page_number)

    context = {
        'author': author,
        'page': page,
        'paginator': paginator,
        'index': True
    }
    return render(request, 'recipe/authorRecipe.html', context=context)


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    context = {
        'recipe': recipe,
        'index': True
    }
    return render(request, 'recipe/singlePage.html', context=context)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        data = request.POST.dict()
        cleaned_data = form.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        cooking_time = cleaned_data.get('cooking_time')
        image = cleaned_data.get('image')
        data_ingredients = functions.get_ingredients_and_validate(data, form)
        ingredients = data_ingredients.get('ingredients')
        data_tags = functions.get_tags_and_validate(data, form)
        tags = data_tags.get('tags')

        if ingredients is None or tags is None:
            form = data_ingredients.get('form') or data_tags.get('form')
            context = {
                'form': form,
                'new_recipe': True
            }
            return render(request, 'recipe/formRecipe.html', context=context)

        recipe = Recipe.objects.create(
            author=request.user,
            title=title,
            description=description,
            cooking_time=cooking_time,
            image=image
        )
        recipe.ingredients.set(ingredients)
        recipe.tag.set(tags)

        return redirect('recipes:index')

    context = {
        'form': form,
        'new_recipe': True
    }
    return render(request, 'recipe/formRecipe.html', context=context)


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user != recipe.author:
        return redirect('recipes:recipe', recipe_id=recipe_id)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    ingredients = functions.get_ingredients_for_edit(recipe)
    tags = functions.get_tags_for_edit(recipe)

    if form.is_valid():
        data = request.POST.dict()
        recipe = form.save(commit=False)
        recipe.author = request.user

        data_ingredients = functions.get_ingredients_and_validate(data, form)
        ingredients = data_ingredients.get('ingredients')
        data_tags = functions.get_tags_and_validate(data, form)
        tags = data_tags.get('tags')

        if ingredients is None or tags is None:
            form = data_ingredients.get('form') or data_tags.get('form')
            context = {
                'form': form,
                'tags': tags,
                'ingredients': ingredients,
                'new_recipe': True,
                'recipe': recipe
            }
            return render(request, 'recipe/formRecipe.html', context=context)

        recipe.ingredients.set(ingredients)
        recipe.tag.set(tags)
        recipe.save()

        return redirect('recipes:index')

    context = {
        'form': form,
        'tags': tags,
        'ingredients': ingredients,
        'new_recipe': True,
        'recipe': recipe
    }
    return render(request, 'recipe/formChangeRecipe.html', context=context)


@login_required
def follows_page(request):
    followings = request.user.follower.all()

    paginator = Paginator(
        followings, recipes_settings.ITEM_RECIPES_FOLLOW
    )
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'follow': True
    }
    return render(request, 'myFollow.html', context=context)


@login_required
def favorite_recipes(request):
    data_get = request.GET

    recipes = functions.get_recipes_by_tag(
        data_get, favorite=True, user=request.user
    )

    paginator = Paginator(
        recipes, recipes_settings.ITEM_RECIPES_FAVORITE
    )
    page_number = data_get.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'favorite': True
    }
    return render(request, 'favorite.html', context=context)


@login_required
def shop_list_page(request):
    recipes = Recipe.objects.filter(
        shoplists__user=request.user
    )

    context = {
        'recipes': recipes,
        'shoplist': True
    }
    return render(request, 'shopList.html', context=context)


@login_required
def shoplist_download(request):
    unprepared_ingredients = Recipe.objects.filter(
        shoplists__user=request.user
    ).values(
        'ingredients__ingredient__title',
        'ingredients__ingredient__dimension',
        'ingredients__quantity'
    )
    ingredients = functions.ingredients_for_download(unprepared_ingredients)
    ingredients = f'Список ингредиентов:\n{ingredients}\n\nFoodGram'

    filename = 'FoodGram_ingredients.txt'
    response = HttpResponse(ingredients, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    Recipe.objects.filter(
        shoplists__user=request.user
    ).delete()

    return response


def delete_recipe(request, recipe_id, username):
    Recipe.objects.filter(id=recipe_id).delete()

    return redirect('recipes:author_page', args=[username])
