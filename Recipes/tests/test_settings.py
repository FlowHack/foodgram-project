from django.test import Client, TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class AllSettings(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = User.objects.create_user(
            username='Akakii',
            email='akakii228@mail.gmail',
            password='password_user'
        )

        #  Клиенты
        cls.guest_client = Client()

        cls.authorized_client = Client()
        cls.authorized_client.force_login(user)
