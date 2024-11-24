from django.db import models

from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(auto_created=True, default=True)
    users = models.ManyToManyField(User, through='ProjectUser')

    def __str__(self):
        return self.name


class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100)

