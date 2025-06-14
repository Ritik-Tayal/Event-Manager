from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Registration
from .forms import EventForm, RegistrationForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import FormView
from .tasks import send_registration_confirmation

class EventListView(View):
    def get(self, request):
        events = Event.objects.all().order_by('start_time')
        return render(request, 'events/event_list.html', {'events': events})

class EventDetailView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        return render(request, 'events/event_detail.html', {'event': event})

class EventCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = EventForm()
        return render(request, 'events/event_create.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event-list')
        return render(request, 'events/event_create.html', {'form': form})

class RegistrationCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.user = request.user
            reg.save()
            send_registration_confirmation.delay(reg.id)
            return redirect('my-registrations')
        return render(request, 'events/register_event.html', {'form': form})

class MyRegistrationsView(LoginRequiredMixin, View):
    def get(self, request):
        registrations = Registration.objects.filter(user=request.user)
        return render(request, 'events/my_registrations.html', {'registrations': registrations})
    
class UserRegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = '/events/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)