# Generated by Django 5.1.3 on 2024-11-16 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chain',
            name='contacts',
            field=models.ManyToManyField(blank=True, null=True, to='retail.contact', verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='chain',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='retail.product', verbose_name='Продукты'),
        ),
    ]
