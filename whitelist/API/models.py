from django.db import models

class WhitelistRequest(models.Model):
    user_name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    addresses = models.TextField(null=True)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        unique_together = ['domain', 'addresses']


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
  
