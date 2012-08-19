from django.contrib import admin
from models import ApiKey

class ApiKeyAdmin(admin.ModelAdmin):
    fields = ('user', 'key', 'notes', 'last_ip', 'last_used', 'created')
    readonly_fields = ('last_ip', 'last_used', 'created')

    def queryset(self, request):
        if request.user.is_superuser:
            return ApiKey.objects.all()

admin.site.register(ApiKey, ApiKeyAdmin)



