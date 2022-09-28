from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client, Contract, Event


admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
