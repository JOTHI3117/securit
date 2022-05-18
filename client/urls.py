from django.urls import path
from . import views

urlpatterns = [
    path('client_login/', views.client_login, name='client_login'),
    path('client_register/', views.client_register, name='client_register'),
    path('client_user/', views.client_user, name='client_user'),
    path('client_logout/', views.client_logout, name='client_logout'),
    path('client_company/', views.client_company, name='client_company'),
    path('search_files/', views.search_files, name='search_files'),
    path('client_request/<int:id>/', views.client_request, name='client_request'),
    path('user_link/', views.user_link, name='user_link'),
    path('question_answer/<int:id>/', views.question_answer, name='question_answer'),
    path('client_view_files/<int:id>/', views.client_view_files, name='client_view_files'),
    path('file_request/<int:id>/', views.file_request, name='file_request'),
    path('file_download/<int:id>/', views.file_download, name='file_download'),
    path('view_gk_question/<int:id>/', views.view_gk_question, name='view_gk_question'),
    path('check_answer/<int:id>/', views.check_answer, name='check_answer'),
    path('different_physical/', views.different_physical, name='different_physical'),
    path('download/<int:id>/', views.download, name='download'),

]
