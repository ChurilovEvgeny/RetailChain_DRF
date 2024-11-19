from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from retail.models import Chain, Product, Contact
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test tests.test_chain - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class ChainTestCaseAuthenticated(APITestCase):

    def setUp(self) -> None:
        self.product_1 = Product.objects.create(
            name="product_1", release_date="2018-03-09"
        )
        self.product_2 = Product.objects.create(
            name="product_2", release_date="2018-03-10"
        )

        self.contact_1 = Contact.objects.create(email="test_1@test.com")
        self.contact_2 = Contact.objects.create(email="test_2@test.com")

        self.chain_1 = Chain.objects.create(name="chain_1")
        self.chain_2 = Chain.objects.create(name="chain_2")
        self.user1 = User.objects.create(username="user1")
        self.client.force_authenticate(user=self.user1)

    def test_chain_str(self):
        user = Chain.objects.get(pk=self.chain_1.pk)
        self.assertEqual(str(user), f"{self.chain_1.name}")

    def test_chain_create(self):
        data = {
            "name": "plant_1",
            "products": [self.product_1.pk, self.product_2.pk],
            "contacts": [self.contact_1.pk, self.contact_2.pk],
            "supplier": self.chain_1.pk,
            "dept": 125.1,
        }
        response = self.client.post(reverse("retail:chain-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chain = Chain.objects.last()
        self.assertEqual(chain.name, data["name"])
        self.assertEqual([i.pk for i in chain.products.all()], data["products"])
        self.assertEqual([i.pk for i in chain.contacts.all()], data["contacts"])
        self.assertEqual(chain.supplier.pk, data["supplier"])
        self.assertEqual(float(chain.dept), data["dept"])

        data = {"name": "plant_2"}
        response = self.client.post(reverse("retail:chain-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chain = Chain.objects.last()
        self.assertEqual(chain.name, data["name"])
        self.assertEqual([i.pk for i in chain.products.all()], [])
        self.assertEqual([i.pk for i in chain.contacts.all()], [])
        self.assertEqual(chain.supplier, None)
        self.assertEqual(float(chain.dept), 0.0)

    def test_chain_list(self):
        response = self.client.get(reverse("retail:chain-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data[0]["name"], self.chain_1.name)
        self.assertEqual(data[1]["name"], self.chain_2.name)

    def test_chain_retrieve(self):
        response = self.client.get(
            reverse("retail:chain-retrieve", args=(self.chain_1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], self.chain_1.name)

    def test_chain_update(self):
        data = {"dept": 1.1}
        response = self.client.patch(
            reverse("retail:chain-update", args=(self.chain_1.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        chain = Chain.objects.get(pk=self.chain_1.pk)
        self.assertEqual(float(chain.dept), data["dept"])

    def test_chain_delete(self):
        response = self.client.delete(
            reverse("retail:chain-delete", args=(self.chain_1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(pk=self.chain_1.pk).exists())


class ChainTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают не авторизованного пользователя"""

    def test_chain_create(self):
        data = {"name": "plant_2"}
        response = self.client.post(reverse("retail:chain-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chain_list(self):
        response = self.client.get(reverse("retail:chain-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chain_retrieve(self):
        response = self.client.get(reverse("retail:chain-retrieve", args=(1111,)))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chain_update(self):
        data = {"dept": 1.1}
        response = self.client.patch(
            reverse("retail:chain-update", args=(1111,)), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chain_delete_self(self):
        response = self.client.delete(reverse("retail:chain-delete", args=(1111,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
