from django.urls import path

from Users import views

app_name = 'users'

urlpatterns = [
    path('auth/signup/', views.SignUp.as_view(), name='signup'),
]
