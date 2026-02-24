from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import User, Property, RentalApplication, Payment
from .models import Message, AgentCommission

# Register models safely to avoid duplicate-registration warnings
for model in (User, Property, RentalApplication, Payment, Message, AgentCommission):
	try:
		admin.site.register(model)
	except AlreadyRegistered:
		pass