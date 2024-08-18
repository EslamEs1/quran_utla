# apps/dashboard/signals.py

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from .models import UserType
from twilio.rest import Client


def send_whatsapp_message(to_number, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body, from_=settings.TWILIO_WHATSAPP_NUMBER, to=to_number
    )
    return message.sid


@receiver(user_logged_in)
def notify_admin_or_manager_login(sender, request, user, **kwargs):
    print(f"User {user.name} with type {user.type} logged in")
    if user.type in [UserType.ADMIN, UserType.MANAGER]:
        message = f"المستخدم {user.name} برقم الهاتف {user.phone} قام بتسجيل الدخول كـ {user.get_type_display()}."
        send_whatsapp_message(settings.YOUR_WHATSAPP_NUMBER, message)
