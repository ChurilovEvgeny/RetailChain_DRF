# Generated by Django 5.1.3 on 2024-11-17 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0003_alter_contact_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['pk'], 'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
    ]