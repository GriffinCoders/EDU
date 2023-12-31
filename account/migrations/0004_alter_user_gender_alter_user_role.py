# Generated by Django 4.2.7 on 2023-11-22 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_created_at_alter_user_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('0', 'Student'), ('1', 'Professor'), ('2', 'IT Manager'), ('3', 'Educational Assistance')], max_length=1),
        ),
    ]
