from django.contrib import admin
from .models import (
    Blood,
    City,
    Hospital,
    RedCross,
    BloodDonor,
    Donation,
    UrgentNeed,
    Campaign,
    ContactMessage,
    BloodStock,
)

def is_coordinator(request):
    return request.user.groups.filter(name='Blood Donation Coordinator').exists()


# Register your models here.
@admin.register(Blood)
class BloodAdmin(admin.ModelAdmin):
    ...


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', )
    ordering = ('order',)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser



@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(RedCross)
class RedCrossAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser



@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer','description', 'location', 'start_time', 'end_time', 'featured', 'featured_order', )
    list_filter = ('location', 'featured', )
    ordering = ('featured_order', )

    def has_add_permission(self, request):
        return request.user.is_superuser or is_coordinator(request)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or is_coordinator(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    ...


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    ...



@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'blood_type', 'units_prefered_number','units_available')
    list_filter = ('hospital', 'blood_type')

    def has_add_permission(self, request):
        return request.user.is_superuser or is_coordinator(request)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or is_coordinator(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or is_coordinator(request)



@admin.register(UrgentNeed)
class UrgentNeedAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'blood_type', 'units_needed', 'blood_stock', 'urgency_level', 'created_at', )
    list_filter = ('urgency_level', 'blood_type')

    def has_add_permission(self, request):
        return request.user.is_superuser or is_coordinator(request)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or is_coordinator(request)

    def has_delete_permission(self, request, obj=None):
        if not (request.user.is_superuser or is_coordinator(request)):
            return False

        # Superuser can always delete
        if request.user.is_superuser:
            return True

        # Coordinator can delete only when enough blood is available
        if obj:
            stock = BloodStock.objects.filter(
                hospital = obj.hospital,
                blood_type = obj.blood_type,
            ).first()

            return (
                    stock is not None
                    and stock.units_available >= obj.units_needed
            )

        return True

    def delete_model(self, request, obj):
        stock = BloodStock.objects.filter(
            hospital = obj.hospital,
            blood_type = obj.blood_type,
        ).first()

        if request.user.is_superuser:
            obj.delete()

        elif(
            is_coordinator(request)
            and stock
            and stock.units_available >= obj.units_needed
        ):
            obj.delete()


    # bulk deletion
    def delete_queryset(self, request, queryset):
        if request.user.is_superuser:
            queryset.delete()
            return

        if is_coordinator(request):
            for obj in queryset:
                stock = BloodStock.objects.filter(
                    hospital = obj.hospital,
                    blood_type = obj.blood_type,
                ).first()

                if (
                    stock
                    and stock.units_available >= obj.units_needed
                ):
                    obj.delete()




@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or is_coordinator(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser




