from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from Recipes.models import Ingredient, Tag

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

        #  Клиенты
        cls.guest_client = Client()

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Tag.objects.all().delete()
        Ingredient.objects.all().delete()
