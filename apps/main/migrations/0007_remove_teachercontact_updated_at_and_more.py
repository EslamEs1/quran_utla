# Generated by Django 5.0.6 on 2024-08-05 15:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_contactus_options_alter_fees_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachercontact',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]