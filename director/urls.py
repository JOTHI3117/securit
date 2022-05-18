from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('director_login/', views.director_login, name='director_login'),
    path('director_user/', views.director_user, name='director_user'),
    path('director_logout/', views.director_logout, name='director_logout'),
    path('company_details_views/', views.company_details_views, name='company_details_views'),
    path('director_approve/<int:id>/', views.director_approve, name='director_approve'),
    path('director_decline/<int:id>/', views.director_decline, name='director_decline'),
    path('view_acceptance/', views.view_acceptance, name='view_acceptance'),
    path('view_format/<int:id>/', views.view_format, name='view_format'),
    path('upload_price/<int:id>/', views.upload_price, name='upload_price'),
    path('send_center/<int:id>/', views.send_center, name='send_center'),
    path('view_temporary_physical/', views.view_temporary_physical, name='view_temporary_physical'),
    path('view_approve_client/<int:id>/', views.view_approve_client, name='view_approve_client'),
    path('send_secure_key/<int:id>/', views.send_secure_key, name='send_secure_key'),
]
