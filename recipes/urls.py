from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('new-recipe/', views.new_recipe, name='new_recipe'),
    path('favorite/', views.favorite_recipes, name='favorite'),
    path('follow/', views.follows_page, name='follow'),
    path('author/<str:username>/', views.author_page, name='author_page'),
    path('recipe/<slug:recipe_slug>/', views.recipe, name='recipe'),
    path(
        'recipe/<slug:recipe_slug>/edit/', views.edit_recipe,
        name='edit_recipe'
    ),
    path(
        'recipe/<slug:recipe_slug>/delete/', views.delete_recipe,
        name='delete_recipe'
    ),
    path('shoplist/', views.shop_list_page, name='shoplist'),
    path(
        'shoplist-download/',
        views.ShoplistPDF.as_view(),
        name='shoplist_download'
    )
]
