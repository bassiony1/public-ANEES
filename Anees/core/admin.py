from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from .models import UserAccount
from rest_framework_simplejwt import token_blacklist
from django.utils.html import format_html, urlencode
from django.urls import reverse
from anees.models import ChildLevel, Child, Level


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = UserAccount
        fields = ("first_name", "last_name", "date_of_birth", "gender", "email")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password1", error)

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserAccount
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("name", "username", "email", "profile", "is_staff", "is_active")

    @admin.display(ordering="first_name")
    def name(self, user):
        return user.get_full_name()

    @admin.display(ordering="first_name")
    def profile(self, user):
        url = (
            reverse("admin:anees_child_changelist")
            + "?"
            + urlencode({"user__id": str(user.id)})
        )
        return format_html('<a href = "{}">{}</a>', url, user.get_full_name())

    list_filter = ("is_staff",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "date_of_birth", "gender")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "gender",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    filter_horizontal = ()


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.register(UserAccount, UserAdmin)
admin.site.unregister(Group)
admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
