from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


    
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_images/user_<id>/<filename>
    return 'profile_images/user_{0}/{1}'.format(instance.user.id, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True, default='')
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    def __str__(self):
        return self.user.username
    




class WritingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=200)
    number_of_words = models.IntegerField()
    duration = models.DurationField()
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='session_photos/', blank=True, null=True)
    start_time = models.DateTimeField()
    excerpt = models.TextField(blank=True)

    def __str__(self):
        return self.session_name