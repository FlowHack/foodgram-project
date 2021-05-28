from django.contrib import admin

from .models import (Favorite, Ingredient, QuantityIngredient, Recipe,
                     ShoppingList, Tag)


@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author', 'title', 'tag')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    empty_value_display = '-пусто-'
