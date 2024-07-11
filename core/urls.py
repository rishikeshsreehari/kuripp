from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('add-session/', views.add_session, name='add_session'),
    path('profile/', views.profile, name='profile'),
    path('', views.landing, name='landing'),
]