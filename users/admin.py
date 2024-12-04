from django.contrib import admin
from .models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_image')
    
    search_fields = ('user__username',)

    list_filter = ('user',)

admin.site.register(Profile, ProfileAdmin)
