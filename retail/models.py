from django.db import models

NULLABLE = {"blank": True, "null": True}


class Contact(models.Model):
    # chain = models.ForeignKey("Chain", related_name="contacts", on_delete=models.SET_NULL, **NULLABLE)

    email = models.EmailField(max_length=255, verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна", default="")
    city = models.CharField(max_length=100, verbose_name="Город", default="")
    street = models.CharField(max_length=100, verbose_name="Улица", default="")
    house_number = models.CharField(
        max_length=10, verbose_name="Номер дома", default=""
    )

    def __str__(self):
        return f"{self.email}: {self.country}, {self.city}, {self.street}, {self.house_number}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["pk"]


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", default="")
    model = models.CharField(max_length=255, verbose_name="Модель", default="")
    release_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Chain(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название цепочки")
    products = models.ManyToManyField(Product, verbose_name="Продукты", **NULLABLE)
    contacts = models.ManyToManyField(Contact, verbose_name="Контакты", **NULLABLE)
    # contacts one to many (related name contacts)
    supplier = models.ForeignKey(
        "Chain", verbose_name="Поставщик", on_delete=models.SET_NULL, **NULLABLE
    )
    dept = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Задолженность", default=0
    )
    creation_date = models.DateTimeField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цепочка"
        verbose_name_plural = "Цепочки"
