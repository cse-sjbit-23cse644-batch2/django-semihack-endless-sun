from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('confirm/<str:hash>/', views.confirm, name='confirm'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('attend/<int:participant_id>/<int:stage_id>/', views.toggle_attendance, name='toggle_attendance'),
    path('feedback/<int:participant_id>/', views.submit_feedback, name='feedback'),
    path('certificate/<str:certificate_hash>/', views.download_certificate, name='certificate'),
    path('verify/<str:certificate_hash>/', views.verify_certificate, name='verify'),
    path('verify-payment/<int:pid>/', views.verify_payment, name='verify_payment'),
]