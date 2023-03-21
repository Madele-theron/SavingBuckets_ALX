from django.contrib import admin

# Register your models here.
from app.models import TotalSaved, SavingGoal

admin.site.register(TotalSaved)
admin.site.register(SavingGoal)
