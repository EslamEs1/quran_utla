# Generated by Django 5.0.6 on 2024-08-03 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_email_contactus_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='slider/img/')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('subject', models.CharField(max_length=200)),
                ('qualifications', models.TextField()),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='pricing',
            name='char',
            field=models.CharField(max_length=2, unique=True),
        ),
    ]