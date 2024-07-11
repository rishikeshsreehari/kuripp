from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from config import FOOTER_TEXT

def landing(request):
    return render(request, 'landing.html', {'footer_text': FOOTER_TEXT})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'footer_text': FOOTER_TEXT, 'title': 'Sign Up', 'button_text': 'Sign Up'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'footer_text': FOOTER_TEXT, 'title': 'Login', 'button_text': 'Login'})

@login_required
def add_session(request):
    if request.method == 'POST':
        form = WritingSessionForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect('profile')
    else:
        form = WritingSessionForm()
    return render(request, 'add_session.html', {'form': form, 'footer_text': FOOTER_TEXT})

@login_required
def profile(request):
    user = request.user
    avatar_url = f"https://avatars.dicebear.com/api/initials/{user.first_name}.svg"
    return render(request, 'profile.html', {'user': user, 'avatar_url': avatar_url, 'footer_text': FOOTER_TEXT})
