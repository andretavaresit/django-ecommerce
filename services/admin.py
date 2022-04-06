from django.contrib import admin

from .models import Service

class ServiceAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'slug')
	class meta:
		model = Service

admin.site.register(Service, ServiceAdmin)