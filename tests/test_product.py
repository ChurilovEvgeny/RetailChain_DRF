import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from retail.models import Product


# python manage.py test - запуск тестов
# python manage.py test tests.test_product - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class ContactTestCaseAuthenticated(APITestCase):

    def setUp(self) -> None:
        self.product_1 = Product.objects.create(name="product_1", release_date="2018-03-09")
        self.product_2 = Product.objects.create(name="product_2", release_date="2018-03-10")
        # self.user1 = User.objects.create(username="user1")
        # self.client.force_authenticate(user=self.user)

    def test_product_str(self):
        user = Product.objects.get(pk=self.product_1.pk)
        self.assertEqual(str(user), f"{self.product_1.name} ({self.product_1.model})")

    def test_product_create(self):
        data = {"name": "test_product_1", "model": "model", "release_date": "2018-03-09"}
        response = self.client.post(reverse("retail:products-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.last()
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.model, data["model"])
        self.assertEqual(product.release_date, datetime.date.fromisoformat(data["release_date"]))

        data = {"name": "test_product_2", "release_date": "2019-03-09"}
        response = self.client.post(reverse("retail:products-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.last()
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.model, "")
        self.assertEqual(product.release_date, datetime.date.fromisoformat(data["release_date"]))

    def test_product_list(self):
        response = self.client.get(reverse("retail:products-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data[0]["name"], self.product_1.name)
        self.assertEqual(data[1]["name"], self.product_2.name)

    def test_product_retrieve_self(self):
        response = self.client.get(reverse("retail:products-detail", args=(self.product_1.pk,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], self.product_1.name)

    def test_product_update_self(self):
        data = {"model": "new_model"}
        response = self.client.patch(
            reverse("retail:products-detail", args=(self.product_1.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product = Product.objects.get(pk=self.product_1.pk)
        self.assertEqual(product.model, data["model"])

    def test_product_delete_self(self):
        response = self.client.delete(
            reverse("retail:products-detail", args=(self.product_1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product_1.pk).exists())

#
#
# class UserTestCaseNotAuthenticated(APITestCase):
#     """Данные тесты описывают не авторизованного пользователя"""
#
#     def setUp(self) -> None:
#         settings.set_testing()
#         self.user = User.objects.create(username="user")
#
#     def test_user_create(self):
#         data = {"username": "user1", "password": "password"}
#         response = self.client.post(reverse("users:users-list"), data=data)
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         user = User.objects.last()
#         self.assertEqual(user.username, data["username"])
#
#     def test_user_list(self):
#         response = self.client.get(reverse("users:users-list"))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_user_retrieve(self):
#         response = self.client.get(reverse("users:users-detail", args=(self.user.pk,)))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_user_update(self):
#         data = {"username": "new_user.ru"}
#         response = self.client.patch(
#             reverse("users:users-detail", args=(self.user.pk,)), data=data
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_user_delete_self(self):
#         response = self.client.delete(
#             reverse("users:users-detail", args=(self.user.pk,))
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
