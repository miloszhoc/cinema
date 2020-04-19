from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = 'Zarządzanie użytkownikami'
admin.site.site_title = 'Użytkownicy'
admin.site.unregister(Group)
UserAdmin.list_filter = ('is_staff', 'is_active', 'groups')
