# Generated by Django 3.2.25 on 2024-03-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_remove_project_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrys',
            name='json',
            field=models.CharField(max_length=10000000),
        ),
    ]
