from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,phone_number ,email,full_name, password=None):

        if not phone_number:
            raise ValueError("Users must have an phone_number")
        if not email:
            raise ValueError("Users must have an email address")
        if not full_name:
            raise ValueError("Users must have an  full_name")
        
        user = self.model(
            email=self.normalize_email(email),
            phone_number = phone_number,
            full_name = full_name          
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone_number, email,full_name, password=None):
        user = self.create_user(
            phone_number,
            email,
            full_name,
            password=password,      
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
