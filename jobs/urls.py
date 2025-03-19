from django.urls import path
from .views import job_list, apply_for_job

urlpatterns = [
    path('', job_list, name='job_list'),
    path('job/<int:job_id>/apply/', apply_for_job, name='apply_for_job'),

]
 