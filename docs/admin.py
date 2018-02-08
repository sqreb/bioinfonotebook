from django.contrib import admin
from .models import SearchTag, InfoTag, MataTag, Doc, DocRel


class DocModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'url', 'public', 'root')


class DocRelModelAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child')


class InfoTagModelAdmin(admin.ModelAdmin):
    list_display = ('tag', 'level')


admin.site.register(Doc, DocModelAdmin)
admin.site.register(DocRel, DocRelModelAdmin)
admin.site.register(SearchTag)
admin.site.register(InfoTag, InfoTagModelAdmin)
admin.site.register(MataTag)
