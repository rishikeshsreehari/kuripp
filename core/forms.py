from django import forms
from .models import WritingSession
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.utils import timezone
       




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['location', 'bio', 'profile_image']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
 


class WritingSessionForm(forms.ModelForm):
    hours = forms.IntegerField(min_value=0, max_value=23, required=False, widget=forms.NumberInput(attrs={'class': 'input input-bordered w-20 text-center', 'placeholder': '00'}))
    minutes = forms.IntegerField(min_value=0, max_value=59, required=False, widget=forms.NumberInput(attrs={'class': 'input input-bordered w-20 text-center', 'placeholder': '00'}))

    class Meta:
        model = WritingSession
        fields = ['session_name', 'number_of_words', 'description', 'photo', 'start_time', 'excerpt']
        widgets = {
            'session_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'number_of_words': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}),
            'photo': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'input input-bordered w-full', 'type': 'datetime-local'}),
            'excerpt': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].initial = timezone.now()

    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('hours', 0)
        minutes = cleaned_data.get('minutes', 0)
        
        if hours is None:
            hours = 0
        if minutes is None:
            minutes = 0
        
        duration = timezone.timedelta(hours=hours, minutes=minutes)
        cleaned_data['duration'] = duration
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.duration = self.cleaned_data['duration']
        if commit:
            instance.save()
        return instance