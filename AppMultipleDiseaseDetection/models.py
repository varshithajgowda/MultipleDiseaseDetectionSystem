from django.db import models

# Create your models here.


class AdminDetails(models.Model):
    Username = models.CharField(max_length=100, default=None)
    Password = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = 'AdminDetails'


class loggedin(models.Model):
    Name = models.CharField(max_length=100, default=None)
    Phone = models.CharField(max_length=100, default=None)
    Email = models.CharField(max_length=100, default=None)
    Username = models.CharField(max_length=100, default=None)
    Password = models.CharField(max_length=100, default=None)
    Address = models.CharField(max_length=100, default=None)
    State = models.CharField(max_length=100, default=None)
    City = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = 'loggedin'


class Hospitals_Data(models.Model):
    hospital_name = models.CharField(max_length=255, default=None)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=100, default=None)
    specialties = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, default=None)
    State = models.CharField(max_length=100, default=None)
    City = models.CharField(max_length=100, default=None)
    Area = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = 'Hospitals_Data'
