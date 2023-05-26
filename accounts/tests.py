from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .models import User

# Create your tests here.

class AccountsTests(APITestCase):
    
    def setUp(self) -> None:
        user = User.objects.create(email="test@test.com",username="test",password="test")
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return super().setUp()
    
    def test_get_user(self):
        response = self.client.get("/api/user/")
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
