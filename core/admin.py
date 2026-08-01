from django.contrib import admin
from .models import Habit, CheckIn, Partnership, Streak

# Register your models here.
admin.site.register(Habit)
admin.site.register(CheckIn)
admin.site.register(Partnership)
admin.site.register(Streak)
