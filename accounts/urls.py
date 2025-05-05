from django.urls import path
from .views import ServiceProviderProfileView

app_name = 'accounts'
 
urlpatterns = [
    path('service-provider/profile/', ServiceProviderProfileView.as_view(), name='service_provider_profile'),
] 