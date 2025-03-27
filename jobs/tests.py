from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Job, JobApplication, Profile
from django.core.cache import cache
import json

class JobViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # self.client.login(username='testuser', password='testpass')

        self.job = Job.objects.create(
            title="Software Engineer",
            company="TechCorp",
            location="Remote",
            description="Job description here",
            salary=50000,
            employment_type="Full-Time",
            industry="Technology",
            experience_level="Entry",
            skills_required="Python, Django",
            user=self.user  # The user is assigned to the job
        )
        self.candidate = User.objects.create_user(username='candidate', password='testpass')
        self.job_application = JobApplication.objects.create(
        job=self.job,
        candidate=self.candidate,
        cover_letter="My cover letter"
        )
        
    
    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_list.html')

    def test_apply_for_job_authenticated(self):
        self.client.login(username='candidate', password='testpass')
        response = self.client.get(reverse('apply_for_job', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)

    def test_apply_for_job_unauthenticated(self):
        job = Job.objects.create(
            title="Test Job", 
            description="Test Description",
            user=self.user  # Assign a user to the job to satisfy NOT NULL constraint
        )  
        response = self.client.get(reverse('apply_for_job', args=[job.id]))
        self.assertEqual(response.status_code, 302)  # redirect to login page

    def test_employer_dashboard_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('employer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/employer_dashboard.html')

    def test_employer_dashboard_unauthenticated(self):
        self.client.login(username='candidate', password='testpass')
        response = self.client.get(reverse('employer_dashboard'))
        self.assertEqual(response.status_code, 302)  # redirect to job_list

    def test_job_detail_view(self):
        response = self.client.get(reverse('job_detail_view', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_detail.html')

    def test_job_list_api_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('job_list_api'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_job_list_api_unauthenticated(self):
        response = self.client.get(reverse('job_list_api'))
        self.assertEqual(response.status_code, 403)
    
    def test_job_application_form_submission(self):
        self.client.login(username='candidate', password='testpass')
        response = self.client.post(reverse('apply_for_job', args=[self.job.id]), {
            'cover_letter': "This is my application",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(JobApplication.objects.filter(candidate=self.candidate, job=self.job).exists())

    def test_message_list_view(self):
        self.client.login(username='candidate', password='testpass')
        response = self.client.get(reverse('message_list', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/message_list.html')