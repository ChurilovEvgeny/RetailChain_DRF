from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from retail.models import Contact
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test tests.test_contact - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class ContactTestCaseAuthenticated(APITestCase):

    def setUp(self) -> None:
        self.contact_1 = Contact.objects.create(email="test_1@test.com")
        self.contact_2 = Contact.objects.create(email="test_2@test.com")
        self.user1 = User.objects.create(username="user1")
        self.client.force_authenticate(user=self.user1)

    def test_contact_str(self):
        user = Contact.objects.get(pk=self.contact_1.pk)
        self.assertEqual(
            str(user),
            f"{self.contact_1.email}: {self.contact_1.country}, {self.contact_1.city}, {self.contact_1.street}, {self.contact_1.house_number}",
        )

    def test_contact_create(self):
        data = {
            "email": "test1@test.com",
            "dept": 200.01,
            "city": "Stalingrad",
            "street": "Lenina str.",
            "country": "USSR",
            "house_number": 17,
        }
        response = self.client.post(reverse("retail:contacts-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contact = Contact.objects.last()
        self.assertEqual(contact.email, data["email"])
        self.assertEqual(contact.country, data["country"])
        self.assertEqual(contact.city, data["city"])
        self.assertEqual(contact.street, data["street"])
        self.assertEqual(contact.house_number, str(data["house_number"]))

        data = {"email": "test2@test.com"}
        response = self.client.post(reverse("retail:contacts-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contact = Contact.objects.last()
        self.assertEqual(contact.email, data["email"])
        self.assertEqual(contact.country, "")
        self.assertEqual(contact.city, "")
        self.assertEqual(contact.street, "")
        self.assertEqual(contact.house_number, "")

    def test_contact_list(self):
        response = self.client.get(reverse("retail:contacts-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data[0]["email"], self.contact_1.email)
        self.assertEqual(data[1]["email"], self.contact_2.email)

    def test_contact_retrieve(self):
        response = self.client.get(
            reverse("retail:contacts-detail", args=(self.contact_1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["email"], self.contact_1.email)

    def test_contact_update(self):
        data = {"email": "new_email@test.com"}
        response = self.client.patch(
            reverse("retail:contacts-detail", args=(self.contact_1.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contact = Contact.objects.get(pk=self.contact_1.pk)
        self.assertEqual(contact.email, data["email"])

    def test_contact_delete(self):
        response = self.client.delete(
            reverse("retail:contacts-detail", args=(self.contact_1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(pk=self.contact_1.pk).exists())


class ContactTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают не авторизованного пользователя"""

    def test_contact_create(self):
        data = {"email": "test2@test.com"}
        response = self.client.post(reverse("retail:contacts-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contact_list(self):
        response = self.client.get(reverse("retail:contacts-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contact_retrieve(self):
        response = self.client.get(reverse("retail:contacts-detail", args=(1111,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contact_update(self):
        data = {"email": "new_email@test.com"}
        response = self.client.patch(
            reverse("retail:contacts-detail", args=(1111,)), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contact_delete_self(self):
        response = self.client.delete(reverse("retail:contacts-detail", args=(1111,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
