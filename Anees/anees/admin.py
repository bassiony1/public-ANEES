from django.contrib import admin
from . import models
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
import nested_admin


# This project uses webpack for building its javascript and css. To install the dependencies for the build process,
# run npm install from the root of the repository. You can then run npm run build to rebuild the static files.


class ChildLevelInline(nested_admin.NestedTabularInline):
    model = models.ChildLevel
    min_num = 1
    extra = 0
    autocomplete_fields = ["level"]


@admin.register(models.Child)
class ChildAdmin(nested_admin.NestedModelAdmin):
    list_display = ["full_name", "age", "gender", "current_level"]
    list_select_related = ["user"]
    list_per_page = 10
    autocomplete_fields = ["user"]

    search_fields = ["user__first_name__icontains", "user__last_name__icontains"]
    inlines = [ChildLevelInline]

    def gender(self, child):
        return child.gender

    @admin.display(ordering="user__date_of_birth")
    def age(self, child):
        return child.age

    @admin.display(ordering="user")
    def full_name(self, child: models.Child):
        return child.full_name

    @admin.display(ordering="current_level")
    def current_level(self, child: models.Child):
        url = (
            reverse("admin:anees_childlevel_changelist")
            + "?"
            + urlencode({"level__level_num": str(child.current_level)})
        )
        return format_html('<a href = "{}">{}</a>', url, child.current_level)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(current_level=Count("levels"))


class ReceptiveImagesInline(nested_admin.NestedTabularInline):
    model = models.ReceptiveImage
    min_num = 0


class SocialConverstionInline(nested_admin.NestedTabularInline):
    model = models.conversionMessage
    min_num = 0


class SocialInline(nested_admin.NestedTabularInline):
    model = models.Social
    inlines = [SocialConverstionInline]
    

class RecptiveInline(nested_admin.NestedTabularInline):
    model = models.Receptive
    inlines = [ReceptiveImagesInline]


class ExpressiveInline(nested_admin.NestedTabularInline):
    model = models.Expressive


@admin.register(models.Level)
class LevelAdmin(nested_admin.NestedModelAdmin):
    list_display = ["level_number", "children"]
    list_filter = ["level_num"]
    list_per_page = 10
    search_fields = ["level_num"]
    inlines = [RecptiveInline, ExpressiveInline, SocialInline]

    @admin.display(ordering="level_num")
    def level_number(self, level):
        return f"Level {level.level_num}"

    @admin.display(ordering="children")
    def children(self, level):
        return level.children_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(children_count=Count("children"))

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["level_num"].initial = models.Level.objects.count() + 1
        form.base_fields["level_num"].disabled = True
        return form


@admin.register(models.ChildLevel)
class ChildLevelAdmin(nested_admin.NestedModelAdmin):
    list_display = [
        "child",
        "level",
        "receptive_complete",
        "expressive_complete",
        "social_complete",
        "completed",
    ]
    list_filter = ["level__level_num"]
    search_fields = [
        "child__user__first_name__icontains",
        "child__user__last_name__icontains",
    ]
    list_select_related = [
        "level__receptive",
        "level__expressive",
        "level__social",
        "child__user",
    ]


@admin.register(models.Receptive)
class ReceptiveAdmin(nested_admin.NestedModelAdmin):
    inlines = [ReceptiveImagesInline]


@admin.register(models.Social)
class SocialAdmin(nested_admin.NestedModelAdmin):
    inlines = [SocialConverstionInline]


admin.site.register(models.Expressive)
admin.site.register(models.ReceptiveImage)
admin.site.register(models.conversionMessage)

# Query set By Age
# class AgeFilter(admin.SimpleListFilter):
#     title = 'Age'
#     parameter_name = 'age'
#     def lookups(self, request, model_admin) :
#         return [
#             ("2" , "2 Years old")
#             # ("3" , "3 Years old")
#             # ("4" , "4 Years old")
#             # ("5" , "5 Years old")
#             # ("6" , "6 Years old")
#             # ("7" , "7 Years old")
#         ]
#     def queryset(self, request, queryset):
#        if self.value == '2' :
#            return queryset.filter(get_age = 2)
