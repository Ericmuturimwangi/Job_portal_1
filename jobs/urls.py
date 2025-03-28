from django.urls import path
from django.contrib.auth import views as auth_views
from .views import job_list, apply_for_job, employer_dashboard, applicant_dashboard, send_message, message_list, JobListView, job_detail_view

urlpatterns = [
    path('', job_list, name='job_list'),
    path('job/<int:job_id>/apply/', apply_for_job, name='apply_for_job'),
    path('dashboard/', employer_dashboard, name='employer_dashboard'),
    path('applicant-dashboard/', applicant_dashboard, name='applicant_dashboard'),
    path('send-message/<int:application_id>/', send_message, name='send_message'),
    path('messages/<int:application_id>/', message_list, name='message_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', auth_views.LoginView.as_view(), name='signup'),
    path('api/jobs/', JobListView.as_view(), name='job_list_api'),
    path('job/<int:job_id>/', job_detail_view, name='job_detail_view'),

]
 