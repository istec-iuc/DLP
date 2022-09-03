from django.contrib import admin
from .models import Logs, Policy, Rule
# Register your models here.

admin.site.register(Logs)
admin.site.register(Rule)
admin.site.register(Policy)