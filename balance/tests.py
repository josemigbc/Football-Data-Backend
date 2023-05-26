from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User
from .models import Balance
# Create your tests here.

class BalanceTests(APITestCase):
    
    def setUp(self) -> None:
        user = User.objects.create(email="test@test.com",username="test",password="test")
        Balance.objects.create(user=user)
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return super().setUp()

    def test_get_balance(self):
        response = self.client.get("/api/balance/")
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['balance'],0)
        self.assertEqual(response.data['user'],1)