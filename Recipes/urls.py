from django.urls import path

from Recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('new-recipe/', views.new_recipe, name='new_recipe'),
    path('favorite/', views.favorite_recipes, name='favorite'),
    path('follow/', views.follows_page, name='follow'),
    path('author/<str:username>', views.author_page, name='author_page'),
    path('recipe/<int:recipe_id>', views.recipe, name='recipe'),
    path('recipe-edit/<int:recipe_id>', views.edit_recipe, name='edit_recipe'),
    path(
        'recipe-delete/<int:recipe_id>/<str:username>', views.delete_recipe,
        name='delete_recipe'
    ),
    path('shoplist/', views.shop_list_page, name='shoplist'),
    path(
        'shoplist-download/', views.shoplist_download, name='shoplist_download'
    )
]
