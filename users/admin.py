from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'phone', 'city', 'avatar', 'is_staff')
    search_fields = ('email', 'username')
    filter_horizontal = ()
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups')}
         ),
    )

    def get_groups_display(self, obj):
        return ", ".join(
            [group.name for group in obj.groups.all()])  # Получаем строковое представление групп пользователя

    get_groups_display.short_description = 'Groups'  # Определяем заголовок для столбца в административной панели


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

