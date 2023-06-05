from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .models import User

# Create your tests here.

class AccountsTests(APITestCase):
    
    def setUp(self) -> None:
        user = User.objects.create_user(email="test@test.com",username="test",password="test")
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return super().setUp()
    
    def test_login_with_ok(self):
        data = {
            "email": "test@test.com",
            "password": "test",
        }
        response = self.client.post("/api/token/",data=data)
        access = response.data.get("access",None)
        refresh = response.data.get("refresh",None)
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        self.assertIsNotNone(access)
        self.assertIsNotNone(refresh)
    
    def test_login_with_wrong_password(self):
        data = {
            "email": "test@test.com",
            "password": "testwrong",
        }
        response = self.client.post("/api/token/",data=data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_login_with_wrong_email(self):
        data = {
            "email": "testwrong@test.com",
            "password": "test",
        }
        response = self.client.post("/api/token/",data=data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_sign_up_with_ok(self):
        data = {
            "username": "test2",
            "email": "test2@gmail.com",
            "password": "testing1234",
        }
        response = self.client.post("/api/signup/",data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    def test_sign_up_without_email(self):
        data = {
            "username": "test2",
            "password": "testing1234",
        }
        response = self.client.post("/api/signup/",data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_sign_up_without_username(self):
        data = {
            "email": "test2@gmail.com",
            "password": "testing1234",
        }
        response = self.client.post("/api/signup/",data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_sign_up_without_password(self):
        data = {
            "email": "test2@gmail.com",
            "username": "test2",
        }
        response = self.client.post("/api/signup/",data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_sign_up_with_same_email(self):
        data = {
            "username": "test2",
            "email": "test@test.com",
            "password": "testing1234",
        }
        response = self.client.post("/api/signup/",data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_sign_up_with_same_username(self):
        data = {
            "username": "test",
            "email": "test2@gmail.com",
            "password": "testing1234",
        }
        response = self.client.post("/api/signup/",data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_get_user(self):
        response = self.client.get("/api/user/")
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
