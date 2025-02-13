from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ("username", "email", "role", "phone_number", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number")
    list_filter = ("role", "is_staff", "is_active")
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "phone_number", "residence_location", "profile_picture")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "phone_number", "is_staff", "is_active"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
