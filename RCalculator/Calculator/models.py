from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)  # DateField for birth date

    def __str__(self):
        return self.name
