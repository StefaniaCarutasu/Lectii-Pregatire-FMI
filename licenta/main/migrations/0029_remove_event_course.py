# Generated by Django 4.0.4 on 2022-06-09 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_event_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='course',
        ),
    ]
