from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _

class CustomSignupForm(SignupForm):
    # Role selection
    is_service_provider = forms.BooleanField(
        required=False,
        label=_("I want to register as a service provider"),
        help_text=_("Check this if you want to offer services on our platform")
    )
    
    # Common fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("First Name")
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Last Name")
    )
    phone_number = forms.CharField(
        max_length=20, 
        required=False,
        label=_("Phone Number")
    )
    
    # Service Provider fields (only required if is_service_provider is True)
    business_name = forms.CharField(
        max_length=255, 
        required=False,
        label=_("Business Name")
    )
    business_description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label=_("Business Description")
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = _("Email Address")
        
    def clean(self):
        cleaned_data = super().clean()
        is_service_provider = cleaned_data.get('is_service_provider')
        
        if is_service_provider:
            # Validate service provider fields
            if not cleaned_data.get('business_name'):
                self.add_error('business_name', _("Business name is required for service providers"))
            if not cleaned_data.get('business_description'):
                self.add_error('business_description', _("Business description is required for service providers"))
        
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        
        # Set common fields
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.phone_number = self.cleaned_data.get('phone_number', '')
        
        # All users are customers by default
        user.add_role('customer')
        
        # If user wants to be a service provider, add that role and set business fields
        if self.cleaned_data.get('is_service_provider'):
            user.add_role('service_provider')
            if user.business_profile:
                user.business_profile.business_name = self.cleaned_data.get('business_name', '')
                user.business_profile.business_description = self.cleaned_data.get('business_description', '')
                user.business_profile.save()
        
        user.save()
        return user 