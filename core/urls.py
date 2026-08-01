from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.habit_list, name='habit_list'),
    path('habits/create/', views.habit_create, name='habit_create'),
    path('habits/<int:pk>/update/', views.habit_update, name='habit_update'),
    path('habits/<int:pk>/delete/', views.habit_delete, name='habit_delete'),

    # CheckIn — nested under a specific habit
    path('habits/<int:pk>/checkins/', views.checkin_list, name='checkin_list'),
    path('habits/<int:habit_id>/checkins/create/', views.checkin_create, name='checkin_create'),
    path('habits/<int:habit_id>/checkins/<int:checkin_id>/update/', views.checkin_update, name='checkin_update'),
    path('habits/<int:habit_id>/checkins/<int:checkin_id>/delete/', views.checkin_delete, name='checkin_delete'),

    path('partnerships/', views.partnership_list, name='partnership_list'),
    path('partnerships/create/', views.partnership_create, name='partnership_create'),
    path('partnerships/<int:pk>/update/', views.partnership_update, name='partnership_update'),
    path('partnerships/<int:pk>/delete/', views.partnership_delete, name='partnership_delete'),
]