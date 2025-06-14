from celery import shared_task
from django.core.mail import send_mail
from .models import Registration

@shared_task
def send_registration_confirmation(registration_id):
    try:
        reg = Registration.objects.select_related('user', 'event').get(id=registration_id)
        subject = f"Registered for {reg.event.title}"
        message = f"Hello {reg.user.username}, you have successfully registered for {reg.event.title} on {reg.event.start_time}."
        recipient = [reg.user.email]
        send_mail(subject, message, 'noreply@eventhub.com', recipient)
    except Registration.DoesNotExist:
        pass