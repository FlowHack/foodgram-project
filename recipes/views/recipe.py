from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from recipes import settings as recipes_settings
from django.forms.utils import ErrorList
from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag
from recipes.views import functions


User = get_user_model()


def index(request):
    data_get = request.GET.dict()

    recipes = functions.get_recipes_by_tags(data_get, Recipe.objects)

    paginator = Paginator(
        recipes, recipes_settings.ITEM_RECIPES_INDEX
    )
    page_number = data_get.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'index': True,
        'tags': Tag.objects.all()
    }
    return render(request, 'recipe/index.html', context=context)


def author_page(request, username):
    data_get = request.GET.dict()
    author = get_object_or_404(User, username=username)
    recipes = functions.get_recipes_by_tags(data_get, author.recipes)

    paginator = Paginator(
        recipes, recipes_settings.ITEM_RECIPES_AUTHOR_PAGE
    )
    page_number = data_get.get('page')
    page = paginator.get_page(page_number)

    context = {
        'author': author,
        'page': page,
        'paginator': paginator,
        'index': True,
        'tags': Tag.objects.all()
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
        recipe = form.save(commit=False)
        recipe.author = request.user

        try:
            error_object = 'ingredients'
            data_ingredients = functions.get_ingredients_and_validate(
                data
            )
            error_object = 'tags'
            tags = functions.get_tags_and_validate(data)
        except ValueError as error:
            form._errors[error_object] = ErrorList(
                [str(error)]
            )
            context = {
                'form': form,
                'new_recipe': True,
                'tags': Tag.objects.all()
            }
            return render(request, 'recipe/formRecipe.html', context=context)

        recipe.save()
        try:
            functions.create_quantity_ingredients(
                data_ingredients, recipe
            )
            recipe.tag.set(tags)
            recipe.save()
        except Exception:
            recipe.delete()

        return redirect('recipes:index')

    context = {'form': form, 'new_recipe': True, 'tags': Tag.objects.all()}
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

    if form.is_valid():
        data = request.POST.dict()
        edit_recipe = form.save(commit=False)
        edit_recipe.author = request.user

        try:
            error_object = 'ingredients'
            data_ingredients = functions.get_ingredients_and_validate(
                data
            )
            error_object = 'tags'
            tags = functions.get_tags_and_validate(data)
        except ValueError as error:
            form._errors[error_object] = ErrorList(
                [str(error)]
            )
            context = {
                'form': form, 'new_recipe': True,
                'recipe': recipe, 'tags': Tag.objects.all()
            }
            return render(
                request, 'recipe/formRecipe.html', context=context
            )

        edit_recipe.save()
        try:
            functions.create_quantity_ingredients(
                data_ingredients, edit_recipe
            )
            edit_recipe.tag.set(tags)
            edit_recipe.save()
        except Exception:
            edit_recipe.delete()

        return redirect('recipes:index')

    context = {
        'form': form, 'new_recipe': True,
        'recipe': recipe, 'tags': Tag.objects.all()
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
    data_get = request.GET.dict()
    recipes = functions.get_recipes_by_tags(
        data_get,
        Recipe.objects.filter(favorites__user=request.user)
    )

    paginator = Paginator(
        recipes, recipes_settings.ITEM_RECIPES_FAVORITE
    )
    page_number = data_get.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'favorite': True,
        'tags': Tag.objects.all()
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
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user != recipe.author:
        return redirect('recipes:recipe', recipe_id=recipe_id)

    recipe.delete()

    return redirect('recipes:author_page', username=request.user.username)


class ShoplistPDF(LoginRequiredMixin, View):
    filename = 'FoodGram_ingredients.pdf'
    template = 'pdf/shoplist.html'

    def get(self, request):
        ingredietns = functions.ingredients_for_download(request.user)
        context = {'ingredients': ingredietns}

        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename=self.filename,
                                       context=context,
                                       show_content_in_browser=False,
                                       )

        return response
