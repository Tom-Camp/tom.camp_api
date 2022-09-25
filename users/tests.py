import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from testing_utils import AuthenticatedAPITestCase, prevent_request_warnings

from users.models import User
from users.serializers import UserSerializer


class GetSingleUserTest(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tester = User.objects.create(
            username="tester",
            first_name="Testy",
            last_name="Testerson",
            email="testing4lyfe@theworldisatest.com",
        )

    def test_get_valid_single_user(self):
        response = self.client.get(
            reverse("user-detail", kwargs={"pk": self.tester.pk})
        )
        user = User.objects.get(pk=self.tester.pk)
        serializer = UserSerializer(user)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @prevent_request_warnings
    def test_get_invalid_single_user(self):
        invalid_id = 0
        response = self.client.get(reverse("user-detail", kwargs={"pk": invalid_id}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewUserTest(APITestCase):
    def test_create_valid_user(self):
        valid_payload = {
            "username": "tester",
            "password": "awesomepassword",
            "first_name": "Testy",
            "last_name": "Testerson",
            "email": "testing4lyfe@theworldisatest.com",
        }

        response = self.client.post(
            reverse("user-list"),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @prevent_request_warnings
    def test_create_invalid_user(self):
        # note that username and password is required for valid post
        invalid_payload = {
            "username": "",
            "first_name": "Testy",
            "last_name": "Testerson",
            "email": "testing4lyfe@theworldisatest.com",
        }

        response = self.client.post(
            reverse("user-list"),
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleUserTest(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.tester = User.objects.create(
            username="tester",
            first_name="Testy",
            last_name="Testerson",
            email="testing4lyfe@theworldisatest.com",
        )

    def test_valid_update_user(self):
        valid_payload = {
            "username": "tester",
            "first_name": "Sleepy",
            "last_name": "Sleeper",
            "email": "naps4ever@iluvnaps.com",
        }
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.tester.pk}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @prevent_request_warnings
    def test_invalid_update_user(self):
        invalid_payload = {
            "username": "",
            "first_name": "Sleepy",
            "last_name": "Sleeper",
            "email": "naps4ever@iluvnaps.com",
        }
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.tester.pk}),
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BasicUserPermissionsTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            username="TestUser", password="supersecretpassword"
        )

    def test_new_user_has_self_permissions(self):
        expected_perms = (
            "view_user",
            "change_user",
            "delete_user",
        )

        self.assertTrue(self.test_user.has_perms(expected_perms, self.test_user))
