import unittest
import json
from rest_framework import status
from rest_framework.test import APITestCase
from requests.auth import HTTPBasicAuth
from django.urls import reverse
from django.contrib.auth.models import User

class TestEventsWithSubscription(APITestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/events-with-subscribers/'
        self.admin = User.objects.create_user('admin', 'admin@test.com', 'password123')
        self.admin.save()
        self.admin.is_staff = True
        self.admin.save()

    def test_success(self):
        url = self.base_url+'27b9fa174d3e8c317f585d3c86cb9d52_14768033385908/'
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertEqual(json.loads(response.getvalue()), {
    "event_id": "27b9fa174d3e8c317f585d3c86cb9d52_14768033385908",
    "names": [
        "API",
        "Michel",
        "Jasper",
        "Bob",
        "Dennis",
        "Edmon",
        "Aslesha",
        "Lars"
    ],
    "title": "Drink a cup of coffee with C42 Team"
})

    def test_wrong_event_id(self):
        url = self.base_url+'27b9fa174d3e8c317f585d3c86cb9d52_14768033385907/'
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        assert response.status_code == 404

    def test_unauthenticated(self):
        url = self.base_url+'27b9fa174d3e8c317f585d3c86cb9d52_14768033385907/'
        response = self.client.get(url)
        assert response.status_code == 403
