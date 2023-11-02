# Generated by Django 4.2.6 on 2023-11-02 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('selection_start', models.DateTimeField()),
                ('selection_finish', models.DateTimeField()),
                ('class_start', models.DateTimeField()),
                ('class_finish', models.DateTimeField()),
                ('substitution_start', models.DateTimeField()),
                ('substitution_finish', models.DateTimeField()),
                ('emergency_removal_finish', models.DateTimeField()),
                ('exams_start', models.DateTimeField()),
                ('term_finish', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('educational_group', models.CharField(max_length=128)),
                ('units', models.PositiveSmallIntegerField()),
                ('grade', models.CharField(max_length=1)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.college')),
            ],
        ),
    ]
