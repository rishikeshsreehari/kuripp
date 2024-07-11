from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class WritingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=255)
    words_written = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField(blank=True, null=True)
    photo = models.ImageField(upload_to='sessions/photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.session_name
