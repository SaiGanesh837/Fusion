# Generated by Django 3.1.5 on 2024-04-22 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globals', '0002_auto_20240420_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='user_status',
            field=models.CharField(choices=[('PRESENT', 'PRESENT'), ('NEW', 'NEW')], default='PRESENT', max_length=50),
        ),
    ]
