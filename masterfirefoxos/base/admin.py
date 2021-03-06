from django.contrib import admin, messages
from django.forms import ValidationError

from feincms.module.medialibrary.admin import MediaFileAdmin as MediaFileAdminOld
from feincms.module.medialibrary.forms import MediaFileAdminForm as MediaFileAdminFormOld

from feincms.module.medialibrary.models import MediaFile
from feincms.module.page.admin import PageAdmin as PageAdminOld
from feincms.module.page.models import Page

from .utils import copy_tree


class PageAdmin(PageAdminOld):
    save_on_top = True
    actions = ['copy_tree_admin_action']
    list_editable = ['in_navigation']
    list_display = ['short_title', 'slug', 'is_visible_admin', 'in_navigation',
                    'template']

    def copy_tree_admin_action(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, 'Select only one page to copy', level=messages.ERROR)
            return
        copy_tree(queryset[0])
    copy_tree_admin_action.short_description = 'Copy tree'


admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)


class MediaFileAdminForm(MediaFileAdminFormOld):
    def clean(self, *args, **kwargs):
        cleaned_data = super(MediaFileAdminForm, self).clean(*args, **kwargs)

        if not cleaned_data.get('categories'):
            raise ValidationError('You must select at least one category.')

        return cleaned_data


class MediaFileAdmin(MediaFileAdminOld):
    form = MediaFileAdminForm
    inlines = []
    list_display = ['admin_thumbnail', '__str__', 'list_categories', 'formatted_created']

    fieldsets = (
        (None, {'fields': ('file', 'categories')}),
    )

    def list_categories(self, obj):
        return ', '.join([category.title for category in obj.categories.all()])


admin.site.unregister(MediaFile)
admin.site.register(MediaFile, MediaFileAdmin)
