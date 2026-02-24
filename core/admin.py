from django.contrib import admin
from .models import User, Property, RentalApplication, Payment

admin.site.register(User)
admin.site.register(Property)
admin.site.register(RentalApplication)
admin.site.register(Payment)