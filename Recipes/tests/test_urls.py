from Recipes.tests.test_settings import AllSettings
from django.urls import reverse


class Addition(AllSettings):
    def check_status_code(self, who, **kwargs):
        """Просмотр статуса доступности страницы для клиента

        Args:
            who (Client): Клиент от которого идёт проверка на доступность
        """
        for url, should_be_status_code in kwargs['kwargs'].items():
            with self.subTest():
                response = who.get(url)
                self.assertEqual(
                    response.status_code,
                    should_be_status_code,
                    f'{url} does not open for unauthorized user'
                )


class StaticURLTests(Addition):
    def test_access_unauthorized(self):
        """
        Тестирование доступности страниц для неавториованных пользователей
        """
        urls: dict[str, int] = {
            reverse('recipes:index'): 200
        }

        self.check_status_code(self.guest_client, kwargs=urls)

    def test_access_authorized(self):
        """
        Тестирование доступности страниц для авторизированных пользователей
        """
        urls: dict[str, int] = {
            reverse('recipes:index'): 200
        }

        self.check_status_code(self.authorized_client, kwargs=urls)

    def test_template(self):
        """
        Тестирование правильности спользования страницами templates
        """
        template_names = {
            reverse('recipes:index'): 'recipe/index.html'
        }

        for reverse_name, template in template_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'Wrong template used for page {reverse_name}'
                )
