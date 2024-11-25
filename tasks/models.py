from django.db import models



class Task(models.Model):
    STATUS_CHOICE = (
        ("PREP", "Подготовка"),
        ("PROG", "В процессе"),
        ("DONE", "Выполнено")
    )
    PRIORITY_CHOICE = (
        ("1", "Низкий"),
        ("2", "Средний"),
        ("3", "Высокий")
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="project")
    users = models.ManyToManyField("users.User", related_name="users", blank=True)
    status = models.CharField(choices=STATUS_CHOICE, max_length=100)
    priority = models.CharField(choices=PRIORITY_CHOICE, max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True)
    testing_responsible = models.ForeignKey("users.User", on_delete=models.SET_NULL, related_name="testing_responsible", null=True)