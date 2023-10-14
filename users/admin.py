from django.contrib import admin

from users.models import User


@admin.register(User)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email',)
    list_filter = ('name',)
    search_fields = ('name', 'surname', 'email')
