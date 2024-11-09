# admin.py
from django.contrib import admin
from .models import MyUser, Profile
from django.utils.translation import gettext_lazy as _
from django.utils import formats

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'email', 'otp_created', 'formatted_date')
    
    def formatted_date(self, obj):
        return formats.date_format(obj.otp_created, "SHORT_DATE_FORMAT")
    
    formatted_date.short_description = _("OTP Created Date")
    search_fields = ['profile__first_name', 'profile__last_name',]

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'first_name', 'last_name', 'formatted_photo_date')
    
#     def formatted_photo_date(self, obj):
#         return formats.date_format(obj.user.date_joined, "SHORT_DATE_FORMAT")
    
#     formatted_photo_date.short_description = _("Date Joined")

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile)
