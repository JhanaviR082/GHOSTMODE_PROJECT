from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserBadge, UserProfile, Badge, DetoxSession, DailyCheckIn

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'dark_mode', 'ghost_avatar')
    fieldsets = UserAdmin.fieldsets + (
        ('GhostMode Settings', {'fields': ('dark_mode', 'ghost_avatar')}),
    )

@admin.register(DetoxSession)
class DetoxSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time', 'duration')

@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'checked_in')
    list_filter = ('user', 'date')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Badge)
admin.site.register(UserProfile)
admin.site.register(UserBadge)
#admin.site.register(DailyCheckIn)