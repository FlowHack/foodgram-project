from django.urls import reverse

from Recipes import settings as recipe_settings
from Recipes.models import (Ingredient, QuantityIngredient, Recipe,
                            ShoppingList, Tag)
from Recipes.tests import constants
from Recipes.tests.test_settings import AllSettings


class Addition(AllSettings):
    @classmethod
    def create_shop_list(*args, **kwargs):
        user = kwargs.get('user')
        recipe = kwargs.get('recipe')

        ShoppingList.objects.create(
            user=user,
            recipe=recipe
        )

    @classmethod
    def create_recipe(*args, **kwargs):
        user = kwargs.get('user')
        data_recipe = kwargs.get('data_recipe')

        __ingredients = Ingredient.objects.filter(
            title__in=list(data_recipe['ingredients'].keys())
        )
        ingredients = [
            QuantityIngredient.objects.get_or_create(
                ingredient=item,
                quantity=data_recipe['ingredients'][item.title]
            )[0] for item in __ingredients
        ]
        recipe = Recipe.objects.create(
            author=user,
            title=data_recipe['title'],
            description=data_recipe['description'],
            cooking_time=data_recipe['cooking_time']
        )
        recipe.ingredients.set(ingredients)
        recipe.tag.set(
            Tag.objects.filter(tag__in=data_recipe['tag'])
        )

        return recipe

    def check_context_page(self, response, check_with, expected_count):
        """
        The function checks context ['page']

        The entrance accepts:
            ~ response - the result of the request
            ~ check_with - what to compare the first post from page to
            ~ expected_count - how many posts should be on one page
        """
        page = response.context['page']
        page_len = len(page)
        first_item = page[0]

        self.assertEqual(first_item, check_with)
        self.assertLessEqual(page_len, expected_count)


class ViewsTest(Addition):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #  Создание рецептов
        for i in range(15):
            data_recipe = constants.recipe_test
            data_recipe['title'] = data_recipe['title'].format(i)
            data_recipe['description'] = data_recipe['description'].format(i)

            cls.recipe_without_image = cls.create_recipe(
                user=cls.user, data_recipe=data_recipe
            )
        cls.recipe_without_image = cls.create_recipe(
            user=cls.user, data_recipe=constants.recipe_1
        )

        #  Создание ShopList
        cls.create_shop_list(
            user=cls.user, recipe=cls.recipe_without_image
        )

    def test_show_correct_context_index(self):
        response = self.authorized_client.get(reverse('recipes:index'))

        count_recipes_all = response.context['paginator'].count

        self.check_context_page(
            response, self.recipe_without_image,
            recipe_settings.ITEM_RECIPES_INDEX,
        )
        self.assertEqual(count_recipes_all, self.user.recipes.count())
