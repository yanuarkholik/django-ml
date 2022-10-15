from django.contrib import admin

# Register your models here.
from .models import Data

@admin.register(Data)
class FileUpload(admin.ModelAdmin):  
    list_display = ('file','file_date', 'id')
    ordering = ('-file_date',)
    search_fields = []

