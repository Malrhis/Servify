from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms

from .models import CustomUser, BusinessProfile

# Create your views here.

class ServiceProviderProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            'business_name',
            'business_description',
            'business_address',
            'business_website',
            'business_hours',
            'facebook',
            'twitter',
            'instagram',
            'linkedin'
        ]
        widgets = {
            'business_description': forms.Textarea(attrs={'rows': 4}),
            'business_address': forms.Textarea(attrs={'rows': 3}),
            'business_hours': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': '{"monday": {"open": "09:00", "close": "17:00"}, ...}'
                }
            ),
        }

    # Add CustomUser fields that we still want to edit
    phone_number = forms.CharField(max_length=20, required=False)
    profile_picture = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['phone_number'].initial = user.phone_number
            self.fields['profile_picture'].initial = user.profile_picture

@method_decorator(login_required, name='dispatch')
class ServiceProviderProfileView(UpdateView):
    form_class = ServiceProviderProfileForm
    template_name = 'accounts/service_provider_profile.html'
    success_url = reverse_lazy('core:dashboard')

    def get_object(self, queryset=None):
        # Get or create business profile
        if not self.request.user.business_profile:
            self.request.user.business_profile = BusinessProfile.objects.create()
            self.request.user.save()
        return self.request.user.business_profile

    def form_valid(self, form):
        response = super().form_valid(form)
        # Update user fields
        user = self.request.user
        user.phone_number = form.cleaned_data['phone_number']
        if form.cleaned_data.get('profile_picture'):
            user.profile_picture = form.cleaned_data['profile_picture']
        user.save()
        
        messages.success(self.request, 'Your profile has been updated successfully!')
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Complete Your Service Provider Profile'
        return context
