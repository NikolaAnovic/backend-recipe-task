from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Email required")
        if not first_name:
            raise ValueError("First name required")
        if not last_name:
            raise ValueError("Last name required")

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(make_password(password))
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):

        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.save()
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=150, unique=True, db_index=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin