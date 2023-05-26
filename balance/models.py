from django.db import models
from accounts.models import User

# Create your models here.

class Balance(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    
