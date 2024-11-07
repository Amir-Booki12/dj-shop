from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User,OptCode
# Register your models here.


class UserAdmin(admin.ModelAdmin):

    
    list_display = ('email','phone_number','is_admin')
    list_filter  = ('is_admin',)
    
  
    
    search_fields = ('email','phone_number')
    ordering = ('full_name',)
    filter_horizontal = ()

@admin.register(OptCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['phone_number','code','created_at']

admin.site.unregister(Group)
admin.site.register(User,UserAdmin)    