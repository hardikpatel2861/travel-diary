from django.db import models
from django.contrib.auth.models import User


# TRIP MODEL
class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')

    title = models.CharField(max_length=200)
    desc = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"