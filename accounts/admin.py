from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'name', 'user_type','visit_fee',
        'phone', 'age', 'gender', 'blood_group', 'created_at'
    )
    list_filter = ('user_type', 'gender', 'blood_group', 'created_at')
    search_fields = ('username', 'email', 'name', 'phone')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password', 'name', 'user_type')
        }),
        ('Personal Details', {
            'fields': ('phone', 'age', 'gender', 'blood_group', 'address', 'bio')
        }),
        ('Doctor Information', {
            'fields': ('specialization', 'license')
        }),
        ('Profile Picture', {
            'fields': ('profile_pic',)
        }),
        ('System Info', {
            'fields': ('created_at',)
        }),
    )
