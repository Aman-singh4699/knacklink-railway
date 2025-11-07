from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import UserTime, AccessRequest


# 🚫 Hide Groups model completely from admin
admin.site.unregister(Group)


# ========================
# Custom simplified User forms
# ========================
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_superuser', 'is_active']

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords don't match")
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']


# ========================
# Minimal User Admin
# ========================
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # rename section in admin sidebar
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        # rename "Users" to "Add Users"
        perms["add_users_label"] = "Add Users"
        return perms


# Unregister the default and re-register
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)


# ========================
# Access Request Admin
# ========================
@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')
    ordering = ('-id',)
    list_per_page = 20


# ========================
# User Time Admin
# ========================
@admin.register(UserTime)
class UserTimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'day_of_week', 'productive_hours', 'target_hours')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)
    ordering = ('-date',)
    list_per_page = 25
