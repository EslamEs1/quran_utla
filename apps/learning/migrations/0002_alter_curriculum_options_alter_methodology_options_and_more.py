# Generated by Django 5.0.6 on 2024-08-05 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curriculum',
            options={'verbose_name_plural': 'Curriculum'},
        ),
        migrations.AlterModelOptions(
            name='methodology',
            options={'verbose_name_plural': 'Methodology'},
        ),
        migrations.AlterModelOptions(
            name='steps_methodology',
            options={'verbose_name_plural': 'Steps Methodology'},
        ),
        migrations.AlterModelOptions(
            name='steps_to_start',
            options={'verbose_name_plural': 'Steps To Start'},
        ),
        migrations.AlterModelOptions(
            name='study_plan',
            options={'verbose_name_plural': 'Study Plan'},
        ),
    ]