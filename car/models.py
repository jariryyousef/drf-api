from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Car(models.Model):
    title = models.CharField(max_length = 64)
    auther = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    descripton = models.TextField()
    year = models.IntegerField(default = None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title