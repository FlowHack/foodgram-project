from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from recipes.models import Ingredient, QuantityIngredient, Recipe, Tag

User = get_user_model()


class AllSettings(TestCase):
    fixtures = [
        'fixtures/ingredients.json',
        'fixtures/tags.json'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='Akakii',
            email='akakii228@mail.gmail',
            password='password_user'
        )
        cls.user_2 = User.objects.create_user(
            username='Akakii_2',
            email='akakii_2@gmail.com',
            password='password_user_2'
        )

        #  Клиенты
        cls.guest_client = Client()

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.authorized_client_without_recipes = Client()
        cls.authorized_client_without_recipes.force_login(cls.user_2)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Tag.objects.all().delete()
        Ingredient.objects.all().delete()

    @classmethod
    def create_recipe(*args, **kwargs):
        user = kwargs.get('user')
        data_recipe = kwargs.get('data_recipe')

        __ingredients = Ingredient.objects.filter(
            title__in=list(data_recipe['ingredients'].keys())
        )
        recipe = Recipe.objects.create(
            author=user,
            title=data_recipe['title'],
            description=data_recipe['description'],
            cooking_time=data_recipe['cooking_time']
        )
        for item in __ingredients:
            QuantityIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=item,
                quantity=data_recipe['ingredients'][item.title]
            )
        recipe.tag.set(
            Tag.objects.filter(tag__in=data_recipe['tag'])
        )

        return recipe
