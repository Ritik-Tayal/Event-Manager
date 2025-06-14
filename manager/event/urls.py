from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    RegistrationCreateView,
    MyRegistrationsView,
    UserRegisterView,
)

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/register/', RegistrationCreateView.as_view(), name='event-register'),
    path('events/my-registrations/', MyRegistrationsView.as_view(), name='my-registrations'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/',UserRegisterView.as_view(), name='register'),
]