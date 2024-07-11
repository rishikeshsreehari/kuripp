from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ensure this line is present
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('add-session/', views.add_session, name='add_session'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),  # Add this line
    
]