from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=255)
    company =models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employment_type = models.CharField(max_length=255, choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Contract', 'Contract')])
    industry = models.CharField(max_length=255)
    experience_level = models.CharField(max_length=100, choices=[('Entry', 'Entry'), ('Mid', 'Mid'), ('Senior', 'Senior')])
    skills_required= models.TextField()
    posted_at= models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

