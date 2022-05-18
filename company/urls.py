from django.urls import path
from . import views

urlpatterns = [
    path('company_login/', views.company_login, name='company_login'),
    path('company_register/', views.company_register, name='company_register'),
    path('company_user/', views.company_user, name='company_user'),
    path('company_logout/', views.company_logout, name='company_logout'),
    path('view_user_company/', views.view_user_company, name='view_user_company'),
    path('view_partner_client/<int:id>/', views.view_partner_client, name='view_partner_client'),
    path('sent_question_link/<int:id>/', views.sent_question_link, name='sent_question_link'),
    path('check_now_mac/<int:id>/', views.check_now_mac, name='check_now_mac'),
]
