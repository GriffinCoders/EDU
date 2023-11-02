# Generated by Django 4.2.6 on 2023-11-02 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('professor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_year', models.PositiveSmallIntegerField(null=True)),
                ('military_status', models.CharField(blank=True, max_length=128, null=True)),
                ('valid_years', models.PositiveSmallIntegerField(default=10)),
                ('grade', models.CharField(choices=[('0', 'Associate'), ('1', 'Undergraduate'), ('2', 'Postgraduate'), ('3', 'Doctoral'), ('4', 'Postdoctoral')], max_length=1)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.college')),
                ('entry_term', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.term')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.field')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='professor.professorprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_text', models.TextField()),
                ('request_title', models.CharField(max_length=128)),
                ('response_text', models.TextField()),
                ('status', models.CharField(choices=[('0', 'Valid'), ('1', 'Deleted'), ('2', 'Pending'), ('3', 'Failed'), ('4', 'Rejected')], max_length=1)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentprofile')),
            ],
        ),
    ]
