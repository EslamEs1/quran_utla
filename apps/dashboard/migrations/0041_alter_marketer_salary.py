# Generated by Django 5.0.6 on 2024-08-11 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0040_alter_marketer_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketer',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]