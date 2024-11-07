from django.db import models
from django.contrib.auth.models  import AbstractBaseUser
from .manager import UserManager
# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='ایمیل کاربری',max_length=255,unique=True)
    phone_number = models.CharField(verbose_name='شماره تماس',max_length=11,unique=True)
    full_name = models.CharField(verbose_name='نام کامل ',max_length=255)
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال',default=True)
    is_admin = models.BooleanField(verbose_name='ادمین',default=False)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email','full_name']
    objects = UserManager()
    
    def __str__(self):
        if self.full_name: return self.full_name
        else: return self.email
     
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True    
     
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class OptCode(models.Model):
    phone_number =models.CharField(verbose_name='شماره تماس',max_length=11)      
    code =models.PositiveIntegerField(verbose_name='کد تایید')      
    created_at =models.DateTimeField(verbose_name='تاریخ ایجاد',auto_now_add=True)      