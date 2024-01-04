from django.db import models

class WhitelistRequest(models.Model):
    user = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    addresses = models.TextField()
    status = models.CharField(max_length=20, default='pending')