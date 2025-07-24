from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_user, name = 'login'),
    path('register/', views.register_user, name = 'register'),
    path('logout/', views.logout_user, name = 'logout'),
    path('verify_otp/', views.verify_otp, name = 'verify_otp'),
    path('chatbot/', views.gemini_chatbot, name = 'chatbot'),
    path('help/', views.help_page, name = 'help'),
    path('resume_builder/', views.resume_builder, name = 'resume_builder'), 
    path('download_pdf/', views.download_resume_pdf, name = 'download_pdf'), 
    path('job_matcher/', views.job_matcher, name = 'job_matcher'),
]