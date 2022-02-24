from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('room/<int:id>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<int:id>/', views.update_room, name='update-room'),
    path('delete-room/<int:id>/', views.delete_room, name='delete-room'),

]
