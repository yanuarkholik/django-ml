from django.db import models

# Create your models here.

class Data(models.Model):
    file = models.FileField()
    file_date = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name