from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, Group
from django.forms.models import BaseModelForm

from .forms import RegisterForm, UserChangeForm
from .models import User, Institution, Donation


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = RegisterForm
    list_display = ['email', 'first_name', 'last_name']
    list_filter = ('is_superuser', )
    ordering = ('email',)
    fieldsets = (
        (None, {
            "fields": (
                ('email', 'first_name', 'last_name', 'is_staff')
            ),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')


admin.site.register(Donation)
admin.site.unregister(Group)
