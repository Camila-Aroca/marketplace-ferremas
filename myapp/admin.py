from django.contrib import admin
from .models import TodoItem, Cliente, TipoTarjeta, Tarjeta

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'genero', 'fecha_nacimiento', 'correo', 'es_miembro')
    search_fields = ('nombre', 'correo')

class TipoTarjetaAdmin(admin.ModelAdmin):
    list_display = ('id_tipo', 'descripcion')
    search_fields = ('id_tipo', 'descripcion')

class TarjetaAdmin(admin.ModelAdmin):
    list_display = ('numero_tarjeta', 'tipo', 'cliente')
    search_fields = ('numero_tarjeta', 'cliente')
    list_filter = ('tipo',)

admin.site.register(TodoItem)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(TipoTarjeta, TipoTarjetaAdmin)
admin.site.register(Tarjeta, TarjetaAdmin)