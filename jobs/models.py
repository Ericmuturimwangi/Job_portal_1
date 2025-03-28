from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.utils import timezone
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

    def __str__ (self):
        return self.title
class Profile (models.Model):
    ROLE_CHOICES =[
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username
    
    

class JobApplication(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='media/applications/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),

    ], default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    job_application =models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} ({self.sent_at})"
    

class JobPerformance(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='performances')
    views = models.PositiveIntegerField(default=0)
    applications = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Performance data for {self.job.title} on {self.date}"
    