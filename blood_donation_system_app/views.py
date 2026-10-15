from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from blood_donation_system_app.forms import ContactMessageForm
from blood_donation_system_app.models import UrgentNeed, Campaign, City
from django.db.models import F


# Create your views here.
def home(request):
    now = timezone.now()
    recent_limit = now - timedelta(days=90)

    # 3 featured campaigns in the order selected by the admin
    campaigns = Campaign.objects.filter(
        featured=True
    ).order_by('featured_order')[:3]

    # Future campaigns
    upcoming_campaigns = Campaign.objects.filter(
        # upcoming campaigns are campaign's that start_time is greater than or equal to now
        start_time__gte=now
    ).order_by('start_time')

    # “Campaigns whose end date is between 90 days ago and now.”
    recent_campaigns = Campaign.objects.filter(
        # recent campaigns are campaigns that end_time is less than or equal to now
        end_time__lte=now,
        # ended no earlier than 90days limit
        end_time__gte=recent_limit
    ).order_by('-end_time')

    return render(request, 'index.html', {
        'campaigns': campaigns,
        'upcoming_campaigns': upcoming_campaigns,
        'recent_campaigns': recent_campaigns,
    })


def about(request):
    return render(request, 'about.html')


def eligibility(request):
    return render(request, 'eligibility.html')


def donate_blood(request):
    return render(request, 'donate_blood.html')


def urgent(request):
    urgent_needs = UrgentNeed.objects.filter(
        units_needed__gt=F('blood_stock__units_available')
    )

    return render(request, 'urgent.html', {
        'urgent_needs': urgent_needs
    })


def locations(request):
    cities = City.objects.all().order_by('order')
    return render(request, 'locations.html',{
        'cities': cities,
    })


def campaigns(request):

    selected_city = request.GET.get('city')

    # newest/latest first(-start_time) ; oldest/earliest first(start_time)
    all_campaigns = Campaign.objects.all().order_by('-date_start', '-start_time')

    if selected_city:
        all_campaigns = all_campaigns.filter(city=selected_city)

    return render(request, 'campaigns.html', {
        'campaigns': all_campaigns,
        'city_choices': Campaign.CITY,
        'selected_city': selected_city,
    })

def campaign_detail(request, id):
    campaign = Campaign.objects.get(id=id)

    return render(request, 'campaign_detail.html', {
        'campaign': campaign
    })



def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect( 'blood_donation_system_app:contact')
    else:
        form = ContactMessageForm()

    return render(request, 'contact.html', {
        'form': form,
    })


