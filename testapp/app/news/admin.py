import json

from django.contrib import admin
from django.utils.safestring import mark_safe
from baton.admin import InputFilter, RelatedDropdownFilter
from rangefilter.filter import DateRangeFilter
from .models import News, Category, Attachment, Video


class TitleFilter(InputFilter):
    parameter_name = 'title'
    title = 'title'

    def queryset(self, request, queryset):
        if self.value() is not None:
            search_term = self.value()
            return queryset.filter(
                title__icontains=search_term
            )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class AttachmentsInline(admin.TabularInline):
    model = Attachment
    extra = 1


class VideosInline(admin.StackedInline):
    model = Video
    extra = 1
    classes = ('collapse-entry', 'expand-first', )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_per_page = 2
    list_display = (
        'title',
        'date',
        'get_category',
        'published',
    )
    list_filter = (
        TitleFilter,
        ('category', RelatedDropdownFilter, ),
        ('date', DateRangeFilter),
        'published',
    )
    inlines = [AttachmentsInline, VideosInline]
    date_hierarchy = 'date'

    fieldsets = (
        ('Dates', {
            'fields': ('date', 'datetime', ),
            'classes': ('order-1', 'baton-tabs-init', 'baton-tab-fs-content', 'baton-tab-fs-flags', 'baton-tab-group-fs-attachments--inline-attachments', 'baton-tab-group-fs-videos--inline-videos'),
            'description': 'This is a description text'

        }),
        ('Main', {
            'fields': (('category', 'title'), 'link', 'content', ),
            'classes': ('tab-fs-content', ),
            'description': 'This is a description text'

        }),
        ('Media', {
            'fields': ('image', ),
            'classes': ('collapse', ),
        }),
        ('Flags', {
            'fields': ('share', 'published', ),
            'classes': ('tab-fs-flags', ),
            'description': 'Set sharing and publishing options'

        }),
        ('Attachments', {
            'fields': ('attachments_summary', ),
            'classes': ('tab-fs-attachments', ),
            'description': 'Add as many attachments as you want'
        }),
        ('Videos', {
            'fields': ('videos_summary', ),
            'classes': ('tab-fs-videos', ),
            'description': 'Add as many videos as you want'

        }),
    )

    baton_form_includes = [
        ('news/admin_datetime_include.html', 'datetime', 'top', ),
        ('news/admin_content_include.html', 'content', 'above', ),
        ('news/admin_title_include.html', 'title', 'right', ),
    ]

    baton_cl_includes = [
        ('news/admin_cl_top_include.html', 'top', ),
    ]

    baton_cl_filters_includes = [
        ('news/admin_cl_filters_top_include.html', 'top', ),
    ]

    def get_category(self, instance):
        return mark_safe('<span class="span-category-id-%d">%s</span>' % (instance.id, str(instance.category)))
    get_category.short_description = 'category'

    def baton_cl_rows_attributes(self, request, cl):
        data = {}
        for news in cl.queryset.filter(category__id=2):
            data[news.id] = {
                'class': 'table-info',
                # 'selector': '#result_list tr input[name=_selected_action][value=%d]' % news.id,
            }
        data[news.id] = {
            'class': 'table-success',
            'selector': '.span-category-id-%d' % 1,
            'getParent': 'td',
            'title': 'A fantasctic tooltip!'
        }
        return json.dumps(data)
