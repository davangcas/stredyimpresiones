from django.contrib import admin

from apps.principal.models.publication import Publication

class PublicacionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'date_created',
        'product',
        'image',
    ]

admin.site.register(Publication, PublicacionAdmin)
