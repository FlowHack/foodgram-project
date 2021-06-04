from django.urls import reverse

from Recipes import settings as recipe_settings
from Recipes.models import Favorite, ShoppingList
from Recipes.tests import constants
from Recipes.tests.test_settings import AllSettings
from Users.models import Follow


class Addition(AllSettings):
    def check_context_page(self, response, check_with, expected_count):
        """Функция проверки context с page

        Args:
            response ([response]): [Ответ сервера]
            check_with ([object]): [С чем сравнивать последний элемент]
            expected_count ([int]): [Ожидаемая длина page]
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
        ShoppingList.objects.create(
            user=cls.user,
            recipe=cls.recipe_without_image
        )

        #  Создание Favorite
        cls.favorite = Favorite.objects.create(
            user=cls.user,
            recipe=cls.recipe_without_image
        )

        #  Создание Follow
        cls.follow = Follow.objects.create(
            user=cls.user_2,
            author=cls.user
        )

    def test_show_correct_context_index(self):
        response = self.authorized_client.get(reverse('recipes:index'))

        count_recipes_all = response.context['paginator'].count
        index = response.context['index']

        self.check_context_page(
            response, self.recipe_without_image,
            recipe_settings.ITEM_RECIPES_INDEX,
        )
        self.assertEqual(count_recipes_all, self.user.recipes.count())
        self.assertEqual(index, True)

    def test_show_correct_context_favorite(self):
        response = self.authorized_client.get(
            reverse('recipes:favorite')
        )

        count_favorites_all = response.context['paginator'].count
        favorite = response.context['favorite']

        self.check_context_page(
            response, self.recipe_without_image,
            recipe_settings.ITEM_RECIPES_FAVORITE
        )
        self.assertEqual(count_favorites_all, self.user.favorites.count())
        self.assertEqual(favorite, True)

    def test_show_crrect_context_follow(self):
        response = self.authorized_client_without_recipes.get(
            reverse('recipes:follow')
        )

        count_followers_all = response.context['paginator'].count
        follow = response.context['follow']

        self.check_context_page(
            response, self.follow,
            recipe_settings.ITEM_RECIPES_FOLLOW
        )
        self.assertEqual(count_followers_all, self.user_2.follower.count())
        self.assertEqual(follow, True)

    def test_show_crrect_context_author_page(self):
        response = self.authorized_client_without_recipes.get(
            reverse('recipes:author_page', args=[self.user.username])
        )

        count_recipes_all = response.context['paginator'].count
        author = response.context['author']
        index = response.context['index']

        self.check_context_page(
            response, self.recipe_without_image,
            recipe_settings.ITEM_RECIPES_AUTHOR_PAGE
        )
        self.assertEqual(count_recipes_all, self.user.recipes.count())
        self.assertEqual(author, self.user)
        self.assertEqual(index, True)

    def test_show_crrect_context_recipe(self):
        response = self.authorized_client_without_recipes.get(
            reverse('recipes:recipe', args=[self.recipe_without_image.id])
        )

        recipe = response.context['recipe']
        index = response.context['index']

        self.assertEqual(recipe, self.recipe_without_image)
        self.assertEqual(index, True)
