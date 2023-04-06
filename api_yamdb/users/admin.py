from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'role',
        'first_name',
        'last_name',
        'email'
    ]
    search_fields = ('role',)
    ordering = ('id',)


admin.site.register(CustomUser, UserAdmin)
