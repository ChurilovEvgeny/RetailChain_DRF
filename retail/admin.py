from django.contrib import admin
from django.db.models import QuerySet

from retail.models import Contact, Product, ChainLink

admin.site.register(Contact)
admin.site.register(Product)


class DeptFilter(admin.SimpleListFilter):
    title = "Задолженность"
    parameter_name = "dept"

    __HAS_DEPT_KEY = "HAS_DEPT"

    def lookups(self, request, model_admin):
        return ((self.__HAS_DEPT_KEY, "Есть задолженность"),)

    def queryset(self, request, queryset):
        if self.value() == self.__HAS_DEPT_KEY:
            return queryset.filter(dept__gt=0)


@admin.action(description="Очистить задолженность перед поставщиком")
def reset_dept(modeladmin, request, queryset: QuerySet):
    for item in queryset:
        item.reset_dept_and_save()


@admin.register(ChainLink)
class ChainLinkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "supplier",
        "dept",
        "creation_date",
    )
    list_filter = ("supplier", "contacts__country", "contacts__city", DeptFilter)
    actions = [
        reset_dept,
    ]
