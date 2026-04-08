from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),

    path('basic_list/<int:pk>/', views.better_menu, name='better_menu'),
    path('add_menu/<int:pk>/', views.add_menu, name='add_menu'),
    path('view_detail/<int:pk>/<int:dish_id>/', views.view_detail, name='view_detail'),
    path('update_dish/<int:pk>/<int:dish_id>/', views.update_dish, name='update_dish'),
    path('delete_dish/<int:pk>/<int:dish_id>/', views.delete_dish, name='delete_dish'),

    path('manage_account/<int:pk>/', views.manage_account, name='manage_account'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    path('delete_account/<int:pk>/', views.delete_account, name='delete_account'),
]
