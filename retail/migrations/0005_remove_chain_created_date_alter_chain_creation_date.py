# Generated by Django 5.1.3 on 2024-11-17 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0004_alter_contact_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chain',
            name='created_date',
        ),
        migrations.AlterField(
            model_name='chain',
            name='creation_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания'),
        ),
    ]
