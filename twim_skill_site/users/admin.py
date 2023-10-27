from django.contrib import admin
from .models import *

admin.site.register(User)


@admin.register(Operations)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'amount', 'type_operations', 'date')
    list_filter = ('type_operations', )
    search_fields = ('user', 'amount', 'date')


@admin.register(TypeOfOperations)
class TypeOfOperationsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(OperationsGame)
class OperationsGameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'operation', 'game')
