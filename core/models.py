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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writing_sessions')
    session_name = models.CharField(max_length=200)
    number_of_words = models.IntegerField()
    duration = models.DurationField(default=datetime.timedelta)  # Ensure you import datetime
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='session_photos/', null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True, default='')

    def save(self, *args, **kwargs):
        self.end_time = self.start_time + self.duration
        super().save(*args, **kwargs)

    def __str__(self):
        return self.session_name
