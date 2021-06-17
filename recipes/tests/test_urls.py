from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.urls import reverse

from recipes.tests import constants
from recipes.tests.test_settings import AllSettings


class Addition(AllSettings):
    def setUp(self):
        super().setUp()
        self.recipe_url = self.create_recipe(
            user=self.user, data_recipe=constants.recipe_url_1
        )
        site = Site.objects.get(pk=1)
        self.flat_about = FlatPage.objects.create(
            url='/about-author/',
            title='about',
            content='<b>content</b>'
        )
        self.flat_spec = FlatPage.objects.create(
            url='/about-spec/',
            title='about spec',
            content='<b>content</b>'
        )
        self.flat_about.sites.add(site)
        self.flat_spec.sites.add(site)

    def check_status_code(self, who, **kwargs):
        """Просмотр статуса доступности страницы для клиента

        Args:
            who (Client): [Клиент от которого идёт проверка на доступность]
            kwargs (dict): [{<url>: <Ожидаемый статус>}]
        """
        for url, should_be_status_code in kwargs['kwargs'].items():
            with self.subTest():
                response = who.get(url)
                self.assertEqual(
                    response.status_code,
                    should_be_status_code,
                    f'{url} does not open for unauthorized user'
                )

    def check_redirects(self, who, **kwargs):
        """Проверка редиректа со страниц

        Args:
            who (Client): [Клиент от которого идёт проверка на доступность]
            kwargs (dict): {<url>: <Куда редирект>}
        """
        for url, redirect in kwargs['kwargs'].items():
            with self.subTest():
                response = who.get(url, follow=True)
                self.assertRedirects(
                    response,
                    redirect
                )

    @staticmethod
    def redirect_url(url, args=None):
        if args is not None:
            return reverse('login') + '?next=' + reverse(url, args=args)

        return reverse('login') + '?next=' + reverse(url)


class StaticURLTests(Addition):
    def test_access_unauthorized(self):
        """
        Тестирование доступности страниц для неавториованных пользователей
        """
        urls = {
            reverse('recipes:index'): 200,
            reverse('recipes:author_page', args=[self.user.username]): 200,
            reverse('recipes:recipe', args=[self.recipe_url.slug]): 200,
            self.flat_about.url: 200,
            self.flat_spec.url: 200,
            'Not_IT_URL': 404
        }

        self.check_status_code(self.guest_client, kwargs=urls)

    def test_unauthorized_redirect(self):
        urls = {
            reverse('recipes:new_recipe'):
                self.redirect_url('recipes:new_recipe'),
            reverse('recipes:follow'):
                self.redirect_url('recipes:follow'),
            reverse('recipes:favorite'):
                self.redirect_url('recipes:favorite'),
            reverse('recipes:shoplist_download'):
                self.redirect_url('recipes:shoplist_download'),
            reverse('recipes:edit_recipe', args=[self.recipe_url.slug]):
                self.redirect_url(
                    'recipes:edit_recipe', args=[self.recipe_url.slug])
        }

        self.check_redirects(self.guest_client, kwargs=urls)

    def test_access_authorized(self):
        """
        Тестирование доступности страниц для авторизированных пользователей
        """
        urls = {
            reverse('recipes:index'): 200,
            reverse('recipes:author_page', args=[self.user.username]): 200,
            reverse('recipes:recipe', args=[self.recipe_url.slug]): 200,
            reverse('recipes:new_recipe'): 200,
            reverse('recipes:follow'): 200,
            reverse('recipes:favorite'): 200,
            reverse('recipes:edit_recipe', args=[self.recipe_url.slug]): 200,
            reverse('recipes:shoplist_download'): 200
        }

        self.check_status_code(self.authorized_client, kwargs=urls)

    def test_authorized_redirect(self):
        urls = {
            reverse('recipes:edit_recipe', args=[self.recipe_url.slug]):
                reverse('recipes:recipe', args=[self.recipe_url.slug]),
        }

        self.check_redirects(
            self.authorized_client_without_recipes, kwargs=urls
        )

    def test_template(self):
        """
        Тестирование правильности спользования страницами templates
        """
        template_names = {
            reverse('recipes:index'): 'recipe/index.html',
            reverse('recipes:new_recipe'): 'recipe/formRecipe.html',
            reverse('recipes:follow'): 'myFollow.html',
            reverse('recipes:favorite'): 'favorite.html',
            reverse('recipes:author_page', args=[self.user.username]):
                'recipe/authorRecipe.html',
            reverse('recipes:recipe', args=[self.recipe_url.slug]):
                'recipe/singlePage.html',
            reverse('recipes:edit_recipe', args=[self.recipe_url.slug]):
                'recipe/formRecipe.html',
            self.flat_about.url: 'flatpages/default.html',
            self.flat_spec.url: 'flatpages/default.html',
        }

        for reverse_name, template in template_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'Wrong template used for page {reverse_name}'
                )
