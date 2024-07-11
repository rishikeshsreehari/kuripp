from django import forms
from .models import WritingSession
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class WritingSessionForm(forms.ModelForm):
    class Meta:
        model = WritingSession
        fields = ['session_name', 'words_written', 'start_time', 'end_time', 'duration', 'photo', 'description', 'excerpt']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input input-bordered w-full'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input input-bordered w-full'}),
            'duration': forms.TimeInput(attrs={'type': 'time', 'class': 'input input-bordered w-full'}),
            'photo': forms.FileInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}),
            'excerpt': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}),
        }


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