# Generated by Django 5.0.6 on 2024-08-27 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_deleteusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
