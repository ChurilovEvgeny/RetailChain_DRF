import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from retail.models import Product
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test tests.test_product - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class ContactTestCaseAuthenticated(APITestCase):

    def setUp(self) -> None:
        self.product_1 = Product.objects.create(
            name="product_1", release_date="2018-03-09"
        )
        self.product_2 = Product.objects.create(
            name="product_2", release_date="2018-03-10"
        )
        self.user1 = User.objects.create(username="user1")
        self.client.force_authenticate(user=self.user1)

    def test_product_str(self):
        user = Product.objects.get(pk=self.product_1.pk)
        self.assertEqual(str(user), f"{self.product_1.name} ({self.product_1.model})")

    def test_product_create(self):
        data = {
            "name": "test_product_1",
            "model": "model",
            "release_date": "2018-03-09",
        }
        response = self.client.post(reverse("retail:products-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.last()
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.model, data["model"])
        self.assertEqual(
            product.release_date, datetime.date.fromisoformat(data["release_date"])
        )

        data = {"name": "test_product_2", "release_date": "2019-03-09"}
        response = self.client.post(reverse("retail:products-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.last()
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.model, "")
        self.assertEqual(
            product.release_date, datetime.date.fromisoformat(data["release_date"])
        )

    def test_product_list(self):
        response = self.client.get(reverse("retail:products-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data[0]["name"], self.product_1.name)
        self.assertEqual(data[1]["name"], self.product_2.name)

    def test_product_retrieve(self):
        response = self.client.get(
            reverse("retail:products-detail", args=(self.product_1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], self.product_1.name)

    def test_product_update(self):
        data = {"model": "new_model"}
        response = self.client.patch(
            reverse("retail:products-detail", args=(self.product_1.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product = Product.objects.get(pk=self.product_1.pk)
        self.assertEqual(product.model, data["model"])

    def test_product_delete(self):
        response = self.client.delete(
            reverse("retail:products-detail", args=(self.product_1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product_1.pk).exists())


class ContactTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают не авторизованного пользователя"""

    def test_product_create(self):
        data = {"name": "test_product_2", "release_date": "2019-03-09"}
        response = self.client.post(reverse("retail:products-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_list(self):
        response = self.client.get(reverse("retail:products-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_retrieve(self):
        response = self.client.get(reverse("retail:products-detail", args=(1111,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_update(self):
        data = {"model": "new_model"}
        response = self.client.patch(
            reverse("retail:products-detail", args=(1111,)), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_delete_self(self):
        response = self.client.delete(reverse("retail:products-detail", args=(1111,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
