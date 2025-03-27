from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Job, Profile, JobApplication
from django.core.cache import cache
import json

class JobViewsTestCase(TestCase):
    def setUp(self):
        # self.client = Client()
        self.employer =User.objects.create_user(username ='employer', password='testpass')
        
        self.employer.profile.role ='employer'
        self.employer.profile.save()

    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_list.html')

    def test_apply_for_job_authenticated(self):
        self.client.login(username='candidate', password='testpass')
        response = self.client.get(reverse('apply_for_job', args=[self.job.id]))
        self.asserEqual(response.status_code, 200)

    def test_apply_for_job_unauthenticated(self):
        response = self.client.get(reverse('apply_for_job', args=[self.job.id]))
        self.assertEqual(response.status_code, 302) #redirect to login page

    def test_employer_dashboard_authenticated(self):
        self.client.login(username='employer', password='testpass')
        response = self.client.get(reverse('employer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/employer_dashboard.html')

    def tes_employer_dashboard_unathorized(self):
        self.client.login(username='candidate', password='testpass')
        response = self.client.get(reverse('employer_dashboard'))
        self.assertEqual(response.status_code, 302)  # redirect to job_list

    def test_job_detail_view(self):
        response = self.client.get(reverse('job_detail_view',args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_detail.html')
    
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
        response = self.client.get(reverse('message_list', args=[self.application.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/message_list.html')
        
        

