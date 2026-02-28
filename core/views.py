from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from reportlab.pdfgen import canvas

from .models import Property, Application, Payment, Message

User = get_user_model()


# =====================================================
# HOME PAGE — PROPERTY LIST
# =====================================================
def home(request):
    properties = Property.objects.all()
    return render(request, "core/home.html", {
        "properties": properties
    })


# =====================================================
# APPLY FOR PROPERTY
# =====================================================
@login_required
def apply_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    application, created = Application.objects.get_or_create(
        tenant=request.user,
        property=prop
    )

    if created:
        messages.success(request, "Application submitted successfully.")
    else:
        messages.warning(request, "You already applied for this property.")

    return redirect("home")


# =====================================================
# PROPERTY DETAIL + APPLY
# =====================================================
@login_required
def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    # Tenant applies
    if request.method == "POST" and request.user.role == "tenant":

        app, created = Application.objects.get_or_create(
            property=prop,
            tenant=request.user
        )

        # Create placeholder payment
        Payment.objects.get_or_create(
            application=app,
            amount=prop.price
        )

        return redirect("application_detail", app_id=app.id)

    return render(request, "core/property_detail.html", {
        "property": prop
    })


# =====================================================
# APPLICATION DETAIL + PDF LEASE
# =====================================================
@login_required
def application_detail(request, app_id):
    app = get_object_or_404(Application, pk=app_id)

    # Generate Lease PDF
    if "generate_pdf" in request.GET:

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="lease_{app.id}.pdf"'

        c = canvas.Canvas(response)

        c.drawString(100, 800, "RentNaija Digital Lease Agreement")
        c.drawString(100, 770, f"Tenant: {app.tenant.username}")
        c.drawString(100, 750, f"Landlord: {app.property.landlord.username}")
        c.drawString(100, 730, f"Property: {app.property.title}")
        c.drawString(100, 710, f"Rent Amount: ₦{app.property.price}")
        c.drawString(100, 690, "Duration: 12 months")

        c.showPage()
        c.save()

        return response

    return render(request, "core/application_detail.html", {
        "application": app
    })


# =====================================================
# LANDLORD DASHBOARD
# =====================================================
@login_required
def landlord_dashboard(request):

    if request.user.role != "landlord":
        return HttpResponse(status=403)

    properties = Property.objects.filter(landlord=request.user)
    applications = Application.objects.filter(
        property__landlord=request.user
    )

    return render(request, "core/landlord_dashboard.html", {
        "properties": properties,
        "applications": applications
    })


# =====================================================
# AGENT DASHBOARD (MVP PLACEHOLDER)
# =====================================================
@login_required
def agent_dashboard(request):

    if request.user.role != "agent":
        return HttpResponse(status=403)

    return render(request, "core/agent_dashboard.html")


# =====================================================
# MESSAGING SYSTEM (BASIC CHAT)
# =====================================================
@login_required
def messages_view(request, user_id):

    receiver = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=request.POST.get("content")
        )

    chats = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by("timestamp")

    return render(request, "core/messages.html", {
        "chats": chats,
        "receiver": receiver
    })


# =====================================================
# PAYMENT CONFIRMATION (TENANT ACTION)
# =====================================================
@login_required
def confirm_payment(request, payment_id):

    payment = get_object_or_404(Payment, id=payment_id)

    if request.user.role == "tenant":
        payment.confirmed = True
        payment.save()
        messages.success(request, "Payment confirmed.")

    return redirect("application_detail", app_id=payment.application.id)