from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cake_requests.models import CakeRequest

from .tasks import (
    create_cake_request,
    delete_cake_request,
    increment_cake_request_access_count,
)


class CakeRequestTests(TestCase):
    def setUp(self):
        # Setup run before every test method.
        CakeRequest.objects.create(
            cake_id=1,
            image_url="http://example.com/cake1.jpg",
            is_cake=True,
            proportion=0.5,
            tolerance=0.1,
            access_count=0,
            status="A",
        )

    def test_create_cake_request(self):
        # Test the create_cake_request task
        create_cake_request(
            2,
            "http://example.com/cake2.jpg",
            0.1,
            {"status_code": 200, "content": {"is_cake": True, "proportion": 0.5}},
        )
        self.assertEqual(CakeRequest.objects.count(), 2)
        new_cake_request = CakeRequest.objects.get(cake_id=2)
        self.assertTrue(new_cake_request.is_cake)

    def test_increment_cake_request_access_count(self):
        # Test the increment_cake_request_access_count task
        increment_cake_request_access_count(1)
        cake_request = CakeRequest.objects.get(cake_id=1)
        self.assertEqual(cake_request.access_count, 1)

    def test_delete_cake_request(self):
        # Test the delete_cake_request task
        delete_cake_request(1)
        cake_request = CakeRequest.objects.get(cake_id=1)
        self.assertEqual(cake_request.status, "D")


class CakeListViewTests(APITestCase):
    @patch("cake_server.views.make_external_api_call.delay")
    def test_get_cakes(self, mock_make_external_api_call):
        # Mock the external API call response
        mock_make_external_api_call.return_value.get.return_value = {
            "status_code": 200,
            "content": [{"id": 1, "name": "Test Cake"}],
        }

        url = reverse("cake-list")  # Replace with your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": 1, "name": "Test Cake"}])


class CakeDetailViewTests(APITestCase):
    @patch("cake_server.views.make_external_api_call.delay")
    def test_get_cake_detail(self, mock_make_external_api_call):
        # Mock the external API call response
        mock_make_external_api_call.return_value.get.return_value = {
            "status_code": 200,
            "content": {"id": 1, "name": "Test Cake"},
            "headers": {"Content-Type": "application/json", "Other-Header": "value"},
        }

        url = reverse(
            "cake-detail", args=[1]
        )  # Replace with your actual URL name and cake_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 1, "name": "Test Cake"})
