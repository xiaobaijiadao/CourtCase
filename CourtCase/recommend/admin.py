from django.contrib import admin

# Register your models here.
from .models import Case

class CaseAdmin(admin.ModelAdmin):
	list_display = ('id','title')
	search_fields = ['title']

admin.site.register(Case, CaseAdmin)