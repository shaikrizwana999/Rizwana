from django.db import models

# Create your models here.

class Station(models.Model):
    Train_Name=models.CharField(max_length=50)
    Train_Number=models.IntegerField()
    Date=models.DateField()
    From_Station=models.CharField(primary_key=True,max_length=50)
    Destination=models.CharField(max_length=50)
    Departure_Time=models.CharField(max_length=50)
    Arrival_Time=models.CharField(max_length=50)
    Duration=models.CharField(max_length=50)
    Quotas=models.CharField(max_length=50)
    Seats=models.IntegerField()
    Price=models.IntegerField()

    def __str__(self):
        return self.Train_Name

from django.contrib.auth.models import User

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to the User model
    From = models.CharField(max_length=100)
    To = models.CharField(max_length=100)
    Phonenumber = models.CharField(max_length=15)
    Email = models.EmailField(max_length=100)
    DepartureDate = models.DateField(null=True)  # Allow null values
    Noofseats = models.IntegerField()
    Quotas = models.CharField(max_length=100)
    Train_Number = models.IntegerField()  # New field for Train Number

    def __str__(self):
        return f'{self.user.username}: {self.From} to {self.To}'

class Contact(models.Model):
    name=models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    msg=models.CharField(max_length=200)

    def __str__(self):
        return self.name