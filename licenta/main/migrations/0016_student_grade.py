# Generated by Django 4.0.4 on 2022-05-31 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_student_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='grade',
            field=models.IntegerField(blank=True, default=12),
            preserve_default=False,
        ),
    ]
