from django.contrib import admin
from .models import General, Weekly


# Register your models here.
class GeneralAdmin(admin.ModelAdmin):
    list_display = ('user', 'winner_hits', 'difference_hits', 'exact_hits', 'points')


class WeeklyAdmin(admin.ModelAdmin):
    list_display = ('week', 'user', 'winner_hits', 'difference_hits', 'exact_hits', 'points')


admin.site.register(General, GeneralAdmin)
admin.site.register(Weekly, WeeklyAdmin)
