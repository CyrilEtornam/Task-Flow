from django.urls import path, include
from users import views

app_name = 'users'
urlpatterns = [
    # Include default urls
    path('', include('django.contrib.auth.urls')),

    # Link to registration page
    path('register/', views.register, name='register'),
]