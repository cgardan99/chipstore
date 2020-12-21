from django.contrib import admin
from .models import Tienda

# Register your models here.
class TiendaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tienda, TiendaAdmin)
