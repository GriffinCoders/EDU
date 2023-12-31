# Generated by Django 4.2.6 on 2023-11-02 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('student', '0002_studentprofile_created_at_studentprofile_updated_at_and_more'),
        ('common', '0002_college_created_at_college_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSelectionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('0', 'Valid'), ('1', 'Deleted'), ('2', 'Pending'), ('3', 'Failed'), ('4', 'Rejected')], max_length=1)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentprofile')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.term')),
            ],
            options={
                'unique_together': {('student', 'term')},
            },
        ),
        migrations.CreateModel(
            name='TermRemovalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('request_text', models.TextField()),
                ('response_text', models.TextField()),
                ('status', models.CharField(choices=[('0', 'Valid'), ('1', 'Deleted'), ('2', 'Pending'), ('3', 'Failed'), ('4', 'Rejected')], max_length=1)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_selection.courseselectionrequest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubstitutionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('0', 'Valid'), ('1', 'Deleted'), ('2', 'Pending'), ('3', 'Failed'), ('4', 'Rejected')], max_length=1)),
                ('added_courses', models.ManyToManyField(related_name='substitution_added', to='course.course')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_selection.courseselectionrequest')),
                ('removed_courses', models.ManyToManyField(related_name='substitution_removed', to='course.course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('passed', models.BooleanField(blank=True, null=True)),
                ('status', models.CharField(choices=[('0', 'Valid'), ('1', 'Deleted'), ('2', 'Pending'), ('3', 'Failed'), ('4', 'Rejected')], max_length=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_selection.courseselectionrequest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseEmergencyRemovalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('request_text', models.TextField()),
                ('response_text', models.TextField()),
                ('status', models.CharField(choices=[('0', 'Valid'), ('1', 'Deleted'), ('2', 'Pending'), ('3', 'Failed'), ('4', 'Rejected')], max_length=1)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_selection.courseselectionrequest')),
                ('removed_courses', models.ManyToManyField(to='course.course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseAppealRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('request_text', models.TextField()),
                ('response_text', models.TextField()),
                ('status', models.CharField(choices=[('0', 'Valid'), ('1', 'Deleted'), ('2', 'Pending'), ('3', 'Failed'), ('4', 'Rejected')], max_length=1)),
                ('student_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_selection.studentcourse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
