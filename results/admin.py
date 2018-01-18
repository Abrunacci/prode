from django.contrib import admin

# Register your models here.
from .models import Result


class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'week', 'user', 'game')

admin.site.register(Result, ResultAdmin)
