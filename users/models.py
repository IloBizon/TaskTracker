from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, password, first_name, last_name):
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    projects = models.ManyToManyField("projects.Project", through="projects.ProjectUser")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name', 'password']
    objects = CustomUserManager()
