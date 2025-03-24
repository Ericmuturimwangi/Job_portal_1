from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, JobApplication, Message
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required
from .forms import JobApplicationForm
import PyPDF2
from django.core.cache import cache

def job_list(request):
    jobs = cache.get('job_list')
    if not jobs:
        jobs = Job.objects.all()
        cache.set('job_list', jobs, timeout=500)

    return render(request, 'jobs/job_list.html', {'jobs':jobs})


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id = job_id)
    form = JobApplicationForm()
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


def parse_pdf(file_path):
    with open (file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text =""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text+= page.extract_text()
        return text
    
@login_required
def send_message(request, application_id):
    application= JobApplication.objects.get(id=application_id)
    if request.method == 'POST':
        content = request.POST.get("content")
        message = Message.objects.create (
            sender = request.user,
            receiver= application.job.user,
            job_application = application,
            content = content,
        )
        return redirect('message_list', application_id = application_id)
    return render(request, 'jobs/send_message.html', {'application': application})

@login_required
def message_list(request, application_id):
    application =  JobApplication.objects.get(id=application_id)
    messages = Message.objects.filter(job_application=application)
    return render(request, 'jobs/message_list.html', {'messages':messages, 'application':application})