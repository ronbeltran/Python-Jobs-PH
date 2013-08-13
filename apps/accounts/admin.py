from django.contrib import admin

from accounts.models import UserProfile

#class UserProfileAdmin(admin.ModelAdmin):
#    list_display = ('url','role',)
#    exclude = ('trusted',)
#    ordering = ('role',)

#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfile)
