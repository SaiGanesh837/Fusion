# Generated by Django 3.1.5 on 2024-02-17 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0003_hidden_grades'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hidden_grades',
            name='grade',
            field=models.CharField(default='C', max_length=5),
        ),
    ]
