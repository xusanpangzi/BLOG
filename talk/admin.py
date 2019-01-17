from django.contrib import admin
from .models import Talk

class TalkAdmin(admin.ModelAdmin):
    list_display = ['body', 'created_time']

admin.site.register(Talk,TalkAdmin)

# Register your models here.
