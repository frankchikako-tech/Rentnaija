from django.contrib import admin
from .models import User, Property, RentalApplication, Lease


# -----------------------------
# USER ADMIN
# -----------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_verified", "is_staff")
    list_filter = ("role", "is_verified", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)


# -----------------------------
# PROPERTY ADMIN
# -----------------------------
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "location",
        "price",
        "is_verified",
        "created_at",
    )
    list_filter = ("is_verified", "location")
    search_fields = ("title", "location", "owner__username")
    list_editable = ("is_verified",)
    ordering = ("-created_at",)


# -----------------------------
# RENTAL APPLICATION ADMIN
# -----------------------------
@admin.register(RentalApplication)
class RentalApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "property",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "tenant__username",
        "property__title",
    )
    list_editable = ("status",)
    ordering = ("-created_at",)


# -----------------------------
# LEASE ADMIN
# -----------------------------
@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "property",
        "start_date",
        "end_date",
        "is_signed",
    )
    list_filter = ("is_signed",)
    search_fields = (
        "tenant__username",
        "property__title",
    )