# models.py
from django.db import models

class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)  # Adjusted field type and length

    def __str__(self):
        return self.username

class Mobile(models.Model):
    title = models.CharField(max_length=255)
    f_rating = models.CharField(max_length=255)
    a_rating = models.CharField(max_length=255)
    f_availability = models.CharField(max_length=255)
    a_availability = models.CharField(max_length=255)
    a_image_url = models.URLField()
    f_product = models.URLField()
    a_product = models.URLField()



    def __str__(self):
        return self.title
