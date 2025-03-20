from django.urls import path
from .views import job_list, apply_for_job, employer_dashboard, applicant_dashboard

urlpatterns = [
    path('', job_list, name='job_list'),
    path('job/<int:job_id>/apply/', apply_for_job, name='apply_for_job'),
    path('dashboard/', employer_dashboard, name='employer_dashboard'),
    path('applicant-dashboard/', applicant_dashboard, name='applicant_dashboard'),


]
 