from django.urls import path

import Recipes.views as views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index')
]
