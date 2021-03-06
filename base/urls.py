from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<int:id>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<int:id>/', views.update_room, name='update-room'),
    path('delete-room/<int:id>/', views.delete_room, name='delete-room'),
    path('user-profile/<int:id>/',views.user_profile,name="user-profile" ),
    path('delete-message/<int:id>/', views.delete_message, name='delete-message'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

]
