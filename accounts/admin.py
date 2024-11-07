from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email','username')
    
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email' ,'password1', 'password2'),
        }),
    )
    
   
    filter_horizontal = ()



admin.site.unregister(Group)
  