from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, JobApplication
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required
from .forms import JobApplicationForm


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs':jobs})


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id = job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application =form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save ()
            return redirect('job_list')
        
        else:
            form = JobApplicationForm()

        return render(request, 'jobs/apply_for_job.html', {'form':form, 'job': job})
@login_required
def employer_dashboard(request):
    if not hasattr(request.user, 'profile'):
        return redirect('create_profile')

    if request.user.profile.role != 'employer':
        return redirect ('job_list')
    

    applications  = JobApplication.objects.filter(job__user = request.user)
    
    return render (request, 'jobs/employer_dashboard.html', {'applications':applications})

@login_required
def applicant_dashboard(request):
    if not hasattr(request.user, 'profile'):
        return redirect('create_profile')
    if request.user.profile.role != 'candidate':
        return redirect ('employer_dashboard')
    
    applications = JobApplication.objects.filter(candidate=request.user)
    return render(request, 'jobs/applicant_dashboard.html', {'applications': applications})