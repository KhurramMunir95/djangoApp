from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('topic/<str:id>', views.GroupDetail, name='User'),
    path('create-group/', views.createGroup, name='create-group'),
    path('update-group/<str:id>', views.updateGroup, name='update-group'),
    path('delete-group/<str:id>', views.deleteGroup, name='delete-group'),
    path('delete-message/<str:id>', views.deleteMessage, name='delete-message'),
    path('register/', views.RegisterUser, name='register'),
    path('login/', views.LoginUser, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
]