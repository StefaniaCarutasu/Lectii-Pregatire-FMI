# Generated by Django 4.0.4 on 2022-06-02 09:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_profile_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursereview',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]