from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('auth/signup/', views.SignUp.as_view(), name='signup'),
]
