from django.contrib import admin

from .models import (Favorite, Ingredient, QuantityIngredient, Recipe,
                     ShoppingList)
from Recipes.forms import RecipeAdminForm
from django.shortcuts import get_object_or_404


@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = ('title', 'author', 'add_to_favorite')
    list_filter = ('author', 'title', 'tag')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'

    def add_to_favorite(self, obj):
        recipe = get_object_or_404(Recipe, id=obj.id)
        return recipe.favorites.all().count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_filter = ('title',)
    earch_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(QuantityIngredient)
class QuantityIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity')
    list_filter = ('ingredient', )
    empty_value_display = '-пусто-'
