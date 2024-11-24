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
    ROLE_CHOICES = (
        ("1", "Младший специалист"),
        ("2", "Специалист"),
        ("3", "Ведущий специалист"),
        ("4", "Главный специалист"),
        ("5", "Руководитель проекта")
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)



class ProjectHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    historical_record = models.CharField(max_length=100)