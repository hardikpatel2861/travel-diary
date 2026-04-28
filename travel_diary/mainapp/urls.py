from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/login/')),   
    path('home/', views.home, name='home'),          
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('edit/<int:id>/', views.edit_trip),
    path('delete/<int:id>/', views.delete_trip),
]