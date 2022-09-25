import json
import time

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User


class UnauthenticatedAPITestCase(APITestCase):
    def test_unauthenticated_request_returns_401(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_token_returns_401(self):
        user, _ = User.objects.get_or_create(username="test-expired", is_superuser=True)
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"TOKEN {token.key}")

        time.sleep(1)

        with self.settings(AUTH_TOKEN_TTL=1 / 60**2):  # 1s
            response = self.client.get("/api/users/")

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            # noinspection PyTypeChecker
            with self.assertRaises(Token.DoesNotExist):
                Token.objects.get(user=user)

    def test_expired_token_is_refreshed_on_successful_auth(self):
        login = json.dumps({"username": "test", "password": "SuperSecretPassword"})

        # Need to create the test user through the client
        create_user = self.client.post("/api/users/", data=login, content_type="application/json")
        self.assertEqual(create_user.status_code, status.HTTP_201_CREATED)

        initial = self.client.post("/api-token-auth/", data=login, content_type="application/json")
        self.assertEqual(initial.status_code, status.HTTP_200_OK)

        initial_token = initial.json()["token"]

        time.sleep(1)

        with self.settings(AUTH_TOKEN_TTL=1 / 60**2):  # 1s
            response = self.client.post("/api-token-auth/", data=login, content_type="application/json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()

        # The expired token will have been refreshed.
        self.assertNotEqual(initial_token, content["token"])

        # noinspection PyTypeChecker
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(key=initial_token)
