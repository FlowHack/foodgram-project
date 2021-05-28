from django.urls import path

from Recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index')
]
