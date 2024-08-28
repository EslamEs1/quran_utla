from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from .models import UserType, Classes


def send_email_notification(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender's email address
        [recipient_email],  # Recipient's email address
        fail_silently=False,
    )


@receiver(user_logged_in)
def notify_admin_or_manager_login(sender, request, user, **kwargs):
    if user.type in [UserType.ADMIN, UserType.MANAGER]:
        subject = "تنبيه تسجيل الدخول للمسؤول/المدير"
        message = f"المستخدم {user.name} برقم الهاتف {user.phone} قام بتسجيل الدخول كـ {user.get_type_display()}."
        send_email_notification(subject, message, settings.NOTIFICATION_EMAIL)


@receiver(post_save, sender=Classes)
def notify_family_on_class_count(sender, instance, **kwargs):
    family = instance.family
    student = instance.student

    # Count the number of classes the student has taken in this family
    class_count = Classes.objects.filter(family=family, student=student).count()

    if class_count == student.count:
        subject = "إشعار إكمال الدروس"
        message = (
            f"تهانينا! الطالب {student.name} من العائلة {family.name} "
            f"أكمل {class_count} دروس."
        )
        try:
            send_email_notification(
                subject, message, settings.FAMILY_NOTIFICATION_EMAIL
            )  # Replace with family's email
            student.count = 0
            student.save()
        except Exception as e:
            print(f"فشل إرسال إشعار البريد الإلكتروني: {e}")
