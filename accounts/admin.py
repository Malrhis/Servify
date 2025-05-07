from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserRole, BusinessProfile, CustomerProfile

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

class BusinessProfileInline(admin.StackedInline):
    model = BusinessProfile
    can_delete = False
    verbose_name = _('Business Profile')
    verbose_name_plural = _('Business Profile')
    fk_name = 'user'

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name = _('Customer Profile')
    verbose_name_plural = _('Customer Profile')
    fk_name = 'user'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'get_roles', 'get_display_name', 'is_active']
    list_filter = ['roles', 'is_active', 'date_joined']
    search_fields = ['email', 'username', 'business_profile__business_name', 'first_name', 'last_name']
    ordering = ['-date_joined']
    filter_horizontal = ('roles', 'groups', 'user_permissions')

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])
    get_roles.short_description = _('Roles')

    def get_display_name(self, obj):
        if obj.is_service_provider and obj.business_profile:
            return obj.business_profile.business_name
        return obj.get_full_name() or obj.email
    get_display_name.short_description = _('Name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')}),
        (_('Roles'), {'fields': ('roles',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        inlines = []
        if obj.is_service_provider:
            inlines.append(BusinessProfileInline(self.model, self.admin_site))
        if obj.is_customer:
            inlines.append(CustomerProfileInline(self.model, self.admin_site))
        return inlines

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['roles'].disabled = True
        return form
