# Generated by Django 4.0.4 on 2022-06-02 10:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(),
        ),
    ]