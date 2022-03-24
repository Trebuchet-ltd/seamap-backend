from django.db import models

image_types = (('test', 'test'),)


# Create your models here
class Image(models.Model):
    name = models.CharField(max_length=15, )
    type = models.CharField(max_length=20, choices=image_types)
    url = models.ImageField(upload_to='images')
