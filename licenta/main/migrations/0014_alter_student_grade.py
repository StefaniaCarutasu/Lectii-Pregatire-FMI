# Generated by Django 4.0.4 on 2022-05-31 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_event_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.IntegerField(blank=True),
        ),
    ]
