# Generated by Django 5.1.3 on 2024-11-25 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retail", "0005_remove_chain_created_date_alter_chain_creation_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChainLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название цепочки"),
                ),
                (
                    "dept",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=15,
                        verbose_name="Задолженность",
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(auto_now=True, verbose_name="Дата создания"),
                ),
                (
                    "contacts",
                    models.ManyToManyField(
                        to="retail.contact", verbose_name="Контакты"
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        to="retail.product", verbose_name="Продукты"
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="retail.chainlink",
                        verbose_name="Поставщик",
                    ),
                ),
            ],
            options={
                "verbose_name": "Звено",
                "verbose_name_plural": "Звенья",
            },
        ),
        migrations.DeleteModel(
            name="Chain",
        ),
    ]