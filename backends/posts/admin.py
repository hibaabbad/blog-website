
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

class AnnoncesAdmin(SummernoteModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    summernote_fields = ('description', )

admin.site.register(Annonces, AnnoncesAdmin)
admin.site.register(Comments)
admin.site.register(Favorite)
admin.site.register(History)