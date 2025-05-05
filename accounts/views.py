from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms

from .models import CustomUser

# Create your views here.

class ServiceProviderProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['business_name', 'business_description', 'profile_picture', 
                 'phone_number', 'address', 'website', 'facebook', 'twitter', 
                 'instagram', 'linkedin']
        widgets = {
            'business_description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

@method_decorator(login_required, name='dispatch')
class ServiceProviderProfileView(UpdateView):
    model = CustomUser
    form_class = ServiceProviderProfileForm
    template_name = 'account/service_provider_profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)
