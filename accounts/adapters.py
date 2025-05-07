from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        user = request.user
        if user.is_service_provider and (not user.business_profile or not user.business_profile.business_name):
            # Redirect service providers to complete their profile
            return reverse('accounts:service_provider_profile')
        return super().get_signup_redirect_url(request) 