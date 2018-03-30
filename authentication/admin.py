from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'nickname', 'reg_date', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'url', 'password')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('必填', {
            'fields': ('email', 'nickname', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'nickname')
    ordering = ('reg_date',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
