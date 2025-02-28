from django.urls import path, include
from .views import *
from .import views
from django.conf import settings
from .views import room_detail, check_availability, submit_booking
from django.views.generic import TemplateView
from django.conf.urls.i18n import set_language

urlpatterns = [
    path("home/", views.home, name='home'),
    path("contact/", views.contactForm, name='contactForm'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path("check-availability/", views.check_availability, name="check_availability"),
    path('booking_form/<str:room_name>/<str:check_in_date>/<str:check_out_date>/', views.submit_booking, name='submit_booking'),
    path('booking-success/', TemplateView.as_view(template_name="booking_success.html"), name="booking_success"),
    path('i18n/', include('django.conf.urls.i18n')),
    path('set-language/', set_language, name='set_language'),
]