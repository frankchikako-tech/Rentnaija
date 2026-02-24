from django.contrib import admin
from .models import User, Property, RentalApplication, Payment
from .models import Message, AgentCommission
admin.site.register(User)
admin.site.register(Property)
admin.site.register(RentalApplication)
admin.site.register(Payment)
admin.site.register(Message)
admin.site.register(AgentCommission)