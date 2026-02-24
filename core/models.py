from django.db import models
from django.contrib.auth.models import AbstractUser

# User with roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
        ('agent', 'Agent'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# Property model
class Property(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=50)
    bedrooms = models.IntegerField()
    image = models.ImageField(upload_to='property_images/')
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Rental Application
class RentalApplication(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='applications')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

# Placeholder for Payment
class Payment(models.Model):
    application = models.OneToOneField(RentalApplication, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)