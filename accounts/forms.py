from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    is_service_provider = forms.BooleanField(required=False)
 
    def save(self, request):
        user = super().save(request)
        user.is_service_provider = self.cleaned_data.get('is_service_provider', False)
        user.save()
        return user 