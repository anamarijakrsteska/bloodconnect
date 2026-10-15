from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blood_donation_system_app import views
from blood_donation_system_app.views import locations

app_name = 'blood_donation_system_app'

urlpatterns = [
        path('', views.home, name='home'),
        path('about/', views.about, name='about'),
        path('eligibility/', views.eligibility, name='eligibility'),
        path('donate_blood/', views.donate_blood, name='donate_blood'),
        path('URGENT/', views.urgent, name='urgent'),
        path('locations/', views.locations, name='locations'),
        path('campaigns/', views.campaigns, name='campaigns'),
        path('campaign/<int:id>/', views.campaign_detail, name='campaign_detail'),
        path('contact/', views.contact, name='contact'),
        #path('login/', views.login, name='login'),
        #path('signup/', views.signup, name='signup')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)