from django.urls import path

from Api import views

app_name = 'api'

urlpatterns = [
    path('purchases/', views.purchases, name='purchases'),
    path('favorites/', views.favorites, name='favorites'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('subscriptions/', views.follow, name='subscriptions')
]
