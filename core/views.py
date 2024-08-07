from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from config import FOOTER_TEXT
from .models import UserProfile, WritingSession  # Import the WritingSession model
from .forms import CustomUserCreationForm, UserProfileForm, UserForm, WritingSessionForm
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404




def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'footer_text': FOOTER_TEXT})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'footer_text': FOOTER_TEXT})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')





from django.shortcuts import render
from .models import WritingSession
from config import FOOTER_TEXT

def home(request):
    if request.user.is_authenticated:
        user = request.user
        writing_sessions = WritingSession.objects.filter(user=user).order_by('-start_time')
        
        for session in writing_sessions:
            duration_hours = session.duration.total_seconds() / 3600  # Convert duration to hours
            if duration_hours > 0:
                session.wph = round(session.number_of_words / duration_hours)
            else:
                session.wph = 0

        return render(request, 'home.html', {
            'writing_sessions': writing_sessions, 
            'footer_text': FOOTER_TEXT
        })
    else:
        return render(request, 'landing.html', {'footer_text': FOOTER_TEXT})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'footer_text': FOOTER_TEXT,
    })

@login_required
def profile(request):
    user = request.user
    profile = user.userprofile

    # Fetching all writing sessions for the logged-in user
    writing_sessions = WritingSession.objects.filter(user=user)

    # Calculating analytics
    number_of_sessions = writing_sessions.count()
    total_words = sum(session.number_of_words for session in writing_sessions)
    avg_wpm = total_words / number_of_sessions if number_of_sessions > 0 else 0

    context = {
        'user': user,
        'profile': profile,
        'number_of_sessions': number_of_sessions,
        'avg_wpm': avg_wpm,
        'current_streak': 0,  # Placeholder for current streak calculation
        'footer_text': FOOTER_TEXT,
    }

    return render(request, 'profile.html', context)

@login_required
@require_POST
def upload_profile_image(request):
    if request.FILES.get('profile_image'):
        request.user.userprofile.profile_image = request.FILES['profile_image']
        request.user.userprofile.save()
    return render(request, 'partials/avatar_container.html', {
        'profile': request.user.userprofile,
        'footer_text': FOOTER_TEXT,
    })

@login_required
@require_POST
def remove_profile_image(request):
    profile = request.user.userprofile
    if profile.profile_image:
        profile.profile_image.delete()
        profile.profile_image = None
        profile.save()
    return render(request, 'partials/avatar_container.html', {'profile': profile})


@login_required
def add_session(request):
    if request.method == 'POST':
        form = WritingSessionForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            messages.success(request, 'Writing session added successfully.')
            return redirect('home')
    else:
        form = WritingSessionForm()
    return render(request, 'add_edit_session.html', {'form': form, 'is_edit': False})

@login_required
def edit_session(request, session_id):
    session = get_object_or_404(WritingSession, id=session_id, user=request.user)
    if request.method == 'POST':
        form = WritingSessionForm(request.POST, request.FILES, instance=session)
        if form.is_valid():
            if request.POST.get('image_clear') == 'true':
                session.photo.delete()
                session.photo = None
            form.save()
            messages.success(request, 'Writing session updated successfully.')
            return redirect('home')
    else:
        form = WritingSessionForm(instance=session)
    return render(request, 'add_edit_session.html', {'form': form, 'is_edit': True, 'session': session})

@login_required
def delete_session(request, session_id):
    session = get_object_or_404(WritingSession, id=session_id, user=request.user)
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Writing session deleted successfully.')
        return redirect('home')
    return render(request, 'delete_session_confirm.html', {'session': session})

