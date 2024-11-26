from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from projects.models import Project
from tasks.models import Task


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, password, first_name, last_name, **kwargs):
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password, first_name, last_name, **kwargs):
        user = self.create_user(username, password, first_name, last_name, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(null=False, blank=False, default="avatar_default.png", upload_to="user_avatars")
    projects = models.ManyToManyField("projects.Project", through="projects.ProjectUser", blank=True)
    tasks = models.ManyToManyField(Task, blank=True)
    comments = models.ManyToManyField("comments.Comment", blank=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name', 'password']
    objects = CustomUserManager()



