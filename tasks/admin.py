from django.contrib import admin
from .models import *
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'status')
    
    list_filter = ('status', 'due_date', 'user')

    search_fields = ('title', 'user__username')

    # Add options for editing directly from the list view
    list_editable = ('status',)

    # Add ordering of the tasks by due_date
    ordering = ('due_date',)

admin.site.register(Task, TaskAdmin)