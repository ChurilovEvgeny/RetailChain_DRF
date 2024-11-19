from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from config import settings
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test tests.test_user - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class UserTestCaseAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя и его же
    доступ к своим же данным"""

    def setUp(self) -> None:
        settings.set_testing()
        self.user = User.objects.create(username="user")
        self.user1 = User.objects.create(username="user1")
        self.client.force_authenticate(user=self.user)

    def test_user_str(self):
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(str(user), user.username)

    def test_user_create(self):
        data = {"username": "user2", "password": "password"}
        response = self.client.post(reverse("users:users-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.last()
        self.assertEqual(user.username, data["username"])

    def test_user_list(self):
        response = self.client.get(reverse("users:users-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            [
                {"id": self.user.pk, "username": self.user.username},
                {"id": self.user1.pk, "username": self.user1.username},
            ],
        )

    def test_user_retrieve_self(self):
        response = self.client.get(reverse("users:users-detail", args=(self.user.pk,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["is_staff"], False)
        self.assertEqual(data["is_active"], True)

    def test_user_retrieve_another(self):
        response = self.client.get(reverse("users:users-detail", args=(self.user1.pk,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data, {"id": self.user1.pk, "username": self.user1.username})

    def test_user_update_self(self):
        data = {"username": "new_user"}
        response = self.client.patch(
            reverse("users:users-detail", args=(self.user.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.username, data["username"])

    def test_user_update_another(self):
        data = {"username": "new_user"}
        response = self.client.patch(
            reverse("users:users-detail", args=(self.user1.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user = User.objects.get(pk=self.user1.pk)
        self.assertEqual(user.username, self.user1.username)

    def test_user_delete_self(self):
        response = self.client.delete(
            reverse("users:users-detail", args=(self.user.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_user_delete_another(self):
        response = self.client.delete(
            reverse("users:users-detail", args=(self.user1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=self.user1.pk).exists())


class UserTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают не авторизованного пользователя"""

    def setUp(self) -> None:
        settings.set_testing()
        self.user = User.objects.create(username="user")

    def test_user_create(self):
        data = {"username": "user1", "password": "password"}
        response = self.client.post(reverse("users:users-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.last()
        self.assertEqual(user.username, data["username"])

    def test_user_list(self):
        response = self.client.get(reverse("users:users-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_retrieve(self):
        response = self.client.get(reverse("users:users-detail", args=(self.user.pk,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update(self):
        data = {"username": "new_user.ru"}
        response = self.client.patch(
            reverse("users:users-detail", args=(self.user.pk,)), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_delete_self(self):
        response = self.client.delete(
            reverse("users:users-detail", args=(self.user.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestJWTTestCase(APITestCase):

    def setUp(self):
        settings.set_testing()
        User.objects.create_user(username="user", password="pass")

    def test_jwt_token(self):
        data = {"username": "user", "password": "pass"}
        response = self.client.post(reverse("users:token"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # access refresh
        data = response.json()
        self.assertTrue("access" in data)
        self.assertTrue("refresh" in data)
        refresh_token = data["refresh"]

        token_refresh_url = reverse("users:token_refresh")
        resp = self.client.post(
            token_refresh_url, {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(token_refresh_url, {"refresh": "abc"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
