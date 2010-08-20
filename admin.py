import csv
from datetime import datetime

from django.http import HttpResponse
from django.contrib import admin

from udoxmailinglist.models import Member, InterestGroup, InterestItem


def export_csv(modeladmin, request, queryset):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=members_%s.csv' % datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    writer = csv.writer(response)
    for row in queryset:
        writer.writerow([
            row.name,
            row.email,
            row.dob.strftime('%Y-%m-%d'),
            row.sex,
            row.mobile,
            ','.join([item.title for item in row.interest_items.order_by('group__pk','pk')],)
        ])
    queryset.update(last_exported=datetime.now())
    return response
export_csv.short_description = "Export as CSV"


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name','email','mobile','join_date','last_exported')
    search_fields = ('name','email')
    list_display_links = ('name', 'email')
    list_filter = ('sex','interest_items','last_exported')
    fieldsets = (
        (None, {'fields': ( 'name',
                            'email',
                            'dob',
                            'sex',
                            'mobile',
                            'interest_items',
                            )
        }),
    )
    actions=[export_csv]
admin.site.register(Member, MemberAdmin)



class InterestGroupAdmin(admin.ModelAdmin):
    list_display = ('sort_weight','title','description')
    search_fields = ('title','description')
    fieldsets = (
        (None, {'fields': ( 'sort_weight',
                            'title',
                            'description',
                            )
        }),
    )
admin.site.register(InterestGroup, InterestGroupAdmin)



class InterestItemAdmin(admin.ModelAdmin):
    list_display = ('sort_weight','title','group','description')
    search_fields = ('title','description')
    list_filter = ('group',)
    fieldsets = (
        (None, {'fields': ( 'sort_weight',
                            'group',
                            'title',
                            'description',
                            )
        }),
    )
admin.site.register(InterestItem, InterestItemAdmin)
