from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class Access_token(models.Model):
#


class Tokens(models.Model):
    user = models.OneToOneField(User, related_name='tokens', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, default="")

    # profile = models.ImageField(upload_to='meadia',blank=True,null=True)

    def __str__(self):
        return f"{self.user} "
