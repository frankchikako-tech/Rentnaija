from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('application/<int:app_id>/', views.application_detail, name='application_detail'),
    path('landlord/', views.landlord_dashboard, name='landlord_dashboard'),
    path('agent/', views.agent_dashboard, name='agent_dashboard'),
    path('messages/<int:user_id>/', views.messages_view, name='messages'),
    path('agent-dashboard/', views.agent_dashboard, name='agent_dashboard'),
]
