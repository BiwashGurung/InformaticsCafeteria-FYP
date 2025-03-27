from django.contrib import admin
from .models import EventPopup
from cafeteria.models import LostFound

admin.site.register(EventPopup)



# Registering the LostFound model with the admin site
# This allows the admin to manage lost and found items through the Django admin interface
@admin.register(LostFound)
class LostFoundAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'user', 'location', 'status', 'submitted_at', 'approved_by')  # Updated from 'student' to 'user'
    list_filter = ('status',)
    search_fields = ('item_name', 'description', 'location')
    actions = ['approve_items', 'mark_resolved']

    def approve_items(self, request, queryset):
        queryset.update(status='approved', approved_by=request.user)
        self.message_user(request, "Selected items have been approved.")
    approve_items.short_description = "Approve selected items"

    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved')
        self.message_user(request, "Selected items marked as resolved.")
    mark_resolved.short_description = "Mark selected items as resolved"