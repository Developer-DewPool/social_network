from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'name', 'is_active')
    search_fields = ('email', 'name',)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
           return True
        else:
           return not obj.is_superuser

admin.site.register(User, UserAdmin)

class AdminFriendRequest(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status']

admin.site.register(FriendRequest, AdminFriendRequest)

