from django.db import models
from django.contrib.auth.models import AbstractUser

# User model.
class User(AbstractUser):

    def __str__(self):
        return self.username