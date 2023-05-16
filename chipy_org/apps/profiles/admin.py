from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role', 'groups')

    def get_search_fields(self, request):
        sfields = super().get_search_fields(request)
        return sfields + ("profile__display_name",)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
