from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

admin.site.site_header = 'Zarządzanie użytkownikami'
admin.site.site_title = 'Użytkownicy'
admin.site.unregister(Group)
UserAdmin.list_filter = ('is_staff', 'is_active', 'groups')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.is_superuser = True
        instance.save()


class NewUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ('user_permissions', 'is_superuser')


class NewUserAdmin(UserAdmin):
    form = NewUserChangeForm
    prepopulated_fields = {'username': ('first_name', 'last_name',)}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2',),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'groups'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
