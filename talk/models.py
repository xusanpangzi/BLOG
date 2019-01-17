from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse

@python_2_unicode_compatible
class Talk(models.Model):
    body=models.TextField()
    created_time=models.DateTimeField()
    def __str__(self):
        return self.body

