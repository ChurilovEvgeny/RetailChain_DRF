from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from retail.models import ChainLink, Product, Contact
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test tests.test_chain_link - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class ChainTestCountryFilter(APITestCase):

    def setUp(self) -> None:
        self.product_1 = Product.objects.create(
            name="product_1", release_date="2018-03-09"
        )
        self.product_2 = Product.objects.create(
            name="product_2", release_date="2018-03-10"
        )

        self.contact_1 = Contact.objects.create(
            email="test_1@test.com", country="Russia"
        )
        self.contact_2 = Contact.objects.create(
            email="test_2@test.com", country="Russia"
        )
        self.contact_3 = Contact.objects.create(email="test_3@test.com", country="USSR")
        self.contact_4 = Contact.objects.create(email="test_4@test.com", country="USA")

        self.chain_1 = ChainLink.objects.create(name="chain_1")
        self.chain_2 = ChainLink.objects.create(name="chain_2")
        self.chain_3 = ChainLink.objects.create(name="chain_3")
        self.chain_4 = ChainLink.objects.create(name="chain_4")

        self.chain_1.contacts.set([self.contact_1.pk, self.contact_3.pk])
        self.chain_1.save()

        self.chain_2.contacts.set(
            [
                self.contact_2.pk,
            ]
        )
        self.chain_2.save()

        self.chain_3.contacts.set(
            [
                self.contact_4.pk,
            ]
        )
        self.chain_3.save()

        self.user1 = User.objects.create(username="user1")
        self.client.force_authenticate(user=self.user1)

    def test_list_without_filter(self):
        response = self.client.get(f'{reverse("retail:chain-list")}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data[0]["name"], self.chain_1.name)
        self.assertEqual(data[1]["name"], self.chain_2.name)
        self.assertEqual(data[2]["name"], self.chain_3.name)
        self.assertEqual(data[3]["name"], self.chain_4.name)

    def test_list_with_filter_no_matches(self):
        response = self.client.get(f'{reverse("retail:chain-list")}?country=China')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 0)

    def test_list_with_filter_have_matches(self):
        response = self.client.get(f'{reverse("retail:chain-list")}?country=Russia')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]["name"], self.chain_1.name)
        self.assertEqual(data[1]["name"], self.chain_2.name)

        response = self.client.get(f'{reverse("retail:chain-list")}?country=Ussr')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)

        self.assertEqual(data[0]["name"], self.chain_1.name)

        response = self.client.get(f'{reverse("retail:chain-list")}?country=USA')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)

        self.assertEqual(data[0]["name"], self.chain_3.name)


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

        self.chain_1 = ChainLink.objects.create(name="chain_1")
        self.chain_2 = ChainLink.objects.create(name="chain_2")
        self.user1 = User.objects.create(username="user1")
        self.client.force_authenticate(user=self.user1)

    def test_chain_str(self):
        user = ChainLink.objects.get(pk=self.chain_1.pk)
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

        chain = ChainLink.objects.last()
        self.assertEqual(chain.name, data["name"])
        self.assertEqual([i.pk for i in chain.products.all()], data["products"])
        self.assertEqual([i.pk for i in chain.contacts.all()], data["contacts"])
        self.assertEqual(chain.supplier.pk, data["supplier"])
        self.assertEqual(float(chain.dept), data["dept"])

        data = {"name": "plant_2"}
        response = self.client.post(reverse("retail:chain-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chain = ChainLink.objects.last()
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

        chain = ChainLink.objects.get(pk=self.chain_1.pk)
        self.assertNotEqual(float(chain.dept), data["dept"])

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
