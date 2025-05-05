from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):
    context = {
        'user': request.user,
    }
    if request.user.is_service_provider:
        # Add service provider specific context here
        context['is_provider'] = True
        # You can add more provider-specific data here
    else:
        # Add regular user specific context here
        context['is_provider'] = False
        # You can add more user-specific data here
    
    return render(request, 'dashboard.html', context)
