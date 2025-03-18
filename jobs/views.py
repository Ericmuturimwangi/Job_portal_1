from django.shortcuts import render
from .models import Job
from django_filters.rest_framework import DjangoFilterBackend


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs':jobs})


