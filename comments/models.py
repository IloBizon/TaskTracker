from django.db import models

class Comment(models.Model):
    task = models.ForeignKey("tasks.Task", on_delete=models.CASCADE, related_name="task")
    author = models.ForeignKey("users.User", on_delete=models.DO_NOTHING, related_name="author")
    comment = models.CharField(max_length=500)

class CommentHistory(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey("users.User", related_name="history_author", on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    comment = models.CharField(max_length=500, null=True)
    historical_record = models.CharField(max_length=100)

