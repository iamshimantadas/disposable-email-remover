from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_args):
        user = self.model(email=self.normalize_email(email), **extra_args)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_args):
        user = self.create_user(email=email, password=password, **extra_args)
        user.is_manager = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user