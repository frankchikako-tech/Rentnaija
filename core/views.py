from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, RentalApplication, Payment, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Message
from django.contrib.auth.decorators import login_required


# Home page: list verified properties
def home(request):
    properties = Property.objects.filter(verified=True)
    return render(request, 'core/home.html', {'properties': properties})

# Property detail and apply
@login_required
def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST' and request.user.role == 'tenant':
        # Create rental application
        app, created = RentalApplication.objects.get_or_create(property=prop, tenant=request.user)
        # Create placeholder payment
        Payment.objects.get_or_create(application=app, amount=prop.price)
        return redirect('application_detail', app_id=app.id)
    return render(request, 'core/property_detail.html', {'property': prop})

# View rental application and generate lease PDF
@login_required
def application_detail(request, app_id):
    app = get_object_or_404(RentalApplication, pk=app_id)
    if 'generate_pdf' in request.GET:
        # Generate simple PDF lease
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="lease_{app.id}.pdf"'
        c = canvas.Canvas(response)
        c.drawString(100, 800, "Digital Lease Agreement")
        c.drawString(100, 780, f"Tenant: {app.tenant.username}")
        c.drawString(100, 760, f"Landlord: {app.property.landlord.username}")
        c.drawString(100, 740, f"Property: {app.property.title}")
        c.drawString(100, 720, f"Rent Amount: ₦{app.property.price}")
        c.drawString(100, 700, "Duration: 12 months")
        c.showPage()
        c.save()
        return response
    return render(request, 'core/application_detail.html', {'application': app})
# Landlord dashboard: view own properties and applications
@login_required
def landlord_dashboard(request):
    if request.user.role != 'landlord':
        return HttpResponse(status=403)
    properties = Property.objects.filter(landlord=request.user)
    applications = RentalApplication.objects.filter(property__landlord=request.user)
    return render(request, 'core/landlord_dashboard.html', {
        'properties': properties,
        'applications': applications,
    })


# Agent dashboard (optional placeholder)
@login_required
def agent_dashboard(request):
    if request.user.role != 'agent':
        return HttpResponse(status=403)
    # future enhancements: show promoted properties, commissions, etc.
    return render(request, 'core/agent_dashboard.html')
@login_required
def messages_view(request, user_id):
    receiver = User.objects.get(id=user_id)

    if request.method == "POST":
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=request.POST.get("content")
        )

    chats = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    return render(request, "core/messages.html", {
        "chats": chats,
        "receiver": receiver
    })
@login_required
def confirm_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)

    if request.user.role == "tenant":
        payment.confirmed = True
        payment.save()

    return redirect('application_detail', app_id=payment.application.id)