from django.db import models
from django.contrib.auth.models  import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(verbose_name='ایمیل کاربری',max_length=255,unique=True)
   