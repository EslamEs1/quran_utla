# Generated by Django 5.0.6 on 2024-09-01 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_student_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='evaluation',
            field=models.CharField(choices=[('Low', 'مقبول'), ('Good', 'جيد'), ('Very Good', 'جيد جدا'), ('Excellence', 'امتياز')], default='Low', max_length=50),
        ),
    ]