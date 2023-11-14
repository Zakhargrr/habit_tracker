from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class HabitTestCase(APITestCase):
    def test_create_user(self):
        user = {
            "first_name": "Test",
            "last_name": "Testov",
            "email": "test@mail.ru",
            "chat_id": "231",
            "password": "12345",
        }

        response = self.client.post(
            '/users/',
            data=user
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
