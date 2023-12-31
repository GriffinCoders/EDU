# Generated by Django 4.2.6 on 2023-11-02 22:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('professor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='professorprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='professorprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
