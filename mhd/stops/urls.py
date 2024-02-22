from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_item, name="add_station"),
    path("station/<int:station_id>", views.detail, name="detail"),
    path("accounts/registration/", views.registration, name="registration"),
]