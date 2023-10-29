from django.urls import path
from . import views

urlpatterns = [
    path('farmers/login/', views.login, name='login'),
    path('farmers/signup/', views.signup, name='signup'),
    path('farmers/logout',views.logout, name='logout'),
    path('farmers/signup/signup',views.signup, name='signup'),
    path('farmers/login/login',views.login, name='login'),
    path('farmers/token/', views.token, name='token'),
    path('farmers/token/token', views.token, name='token'),
    path('initialize_time_slots/', views.initialize_time_slots, name='initialize_time_slots'),
]
