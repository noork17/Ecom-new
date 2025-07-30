from django.urls import path
from .views import index,register,password_reset,activation_email
from .views import home

urlpatterns = [
    path('', index, name='login'),
path('register/', register, name='register'),
    path('password_reset/', password_reset, name='password_reset'),
    path('activate/<str:email_token>/',activation_email,name='activation_email_par'),
    path('home/',home,name='home'),

]
