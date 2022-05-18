from django.urls import path
from . import views

urlpatterns = [
    path('center_login/', views.center_login, name='center_login'),
    path('center_register/', views.center_register, name='center_register'),
    path('center_user/', views.center_user, name='center_user'),
    path('center_logout/', views.center_logout, name='center_logout'),
    path('view_director_send/<int:id>/', views.view_director_send, name='view_director_send'),
    path('encrypt_file/<int:id>/', views.encrypt_file, name='encrypt_file'),
    path('user_request/<int:id>/', views.user_request, name='user_request'),
    path('generator_key/<int:id>/', views.generator_key, name='generator_key'),
    path('view_client_request/<int:id>/', views.view_client_request, name='view_client_request'),
    path('check_mac/<int:id>/', views.check_mac, name='check_mac'),
    path('view_director_accept/', views.view_director_accept, name='view_director_accept'),
    path('view_director_user/', views.view_director_user, name='view_director_user'),
    path('director_user_accept/', views.director_user_accept, name='director_user_accept'),
    path('send_to_organization/<int:id>/', views.send_to_organization, name='send_to_organization'),

]
