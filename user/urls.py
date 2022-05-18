from django.urls import path
from . import views

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_main/', views.user_main, name='user_main'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('company_details/', views.company_details, name='company_details'),
    path('view_director/', views.view_director, name='view_director'),
    path('file_details/<int:id>/', views.file_details, name='file_details'),
    path('price_accept/<int:id>/', views.price_accept, name='price_accept'),
    path('price_deny/<int:id>/', views.price_deny, name='price_deny'),
    path('approve_file/', views.approve_file, name='approve_file'),
    path('file_upload/<int:id>/', views.file_upload, name='file_upload'),
    path('requests_file/<int:id>/', views.requests_file, name='requests_file'),
    path('data_send/', views.data_send, name='data_send'),
    path('view_decrypt_file/<int:id>/', views.view_decrypt_file, name='view_decrypt_file'),
    path('view_user_question/', views.view_user_question, name='view_user_question'),
    path('view_question/', views.view_question, name='view_question'),
    path('question/', views.question, name='question'),
    path('client_request/', views.client_request, name='client_request'),
    path('client_accept/<int:id>/', views.client_accept, name='client_accept'),
    path('client_deny/<int:id>/', views.client_deny, name='client_deny'),
    path('send_link/<int:id>/', views.send_link, name='send_link'),
    path('view_change_client/', views.view_change_client, name='view_change_client'),
    path('approve/<int:id>/', views.approve, name='approve'),
    path('deny/<int:id>/', views.deny, name='deny'),
]
