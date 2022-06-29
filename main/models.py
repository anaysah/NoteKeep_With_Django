from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    data = models.CharField(max_length = 200)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.id