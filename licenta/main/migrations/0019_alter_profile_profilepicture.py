# Generated by Django 4.0.4 on 2022-06-01 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profilePicture',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
