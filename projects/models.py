from django.db import models

from tasks.models import Task


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(auto_created=True, default=True)
    users = models.ManyToManyField("users.User", through='ProjectUser')
    tasks = models.ManyToManyField(Task, related_name="project_tasks", blank=True)

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
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)



class ProjectHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    historical_record = models.CharField(max_length=100)