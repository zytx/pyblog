from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm,UserChangeForm

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'nikename', 'reg_date', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('nikename','email', 'url','password')}),
        ('权限', {'fields': ('is_active','is_staff','is_superuser','groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('必填', {
            'fields': ('email', 'nikename', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','nikename')
    ordering = ('reg_date',)
    filter_horizontal = ('groups', 'user_permissions',)



admin.site.register(User, UserAdmin)