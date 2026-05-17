from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    deadline = models.DateField(null=True, blank=True)  # NEW
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Step(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title