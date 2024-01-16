from django.contrib import admin

from .models import Station

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass