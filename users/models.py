from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    AUTHOR = 'author'
    READER = 'reader'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (AUTHOR, 'Author'),
        (READER, 'Reader'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def is_admin(self):
        return self.role == self.ADMIN

    def is_author(self):
        return self.role == self.AUTHOR

    def is_reader(self):
        return self.role == self.READER
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username