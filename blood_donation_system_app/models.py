from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


# Create your models here.
class Blood(models.Model):
    BLOOD_TYPES = [
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
    ]
    blood_type = models.CharField(max_length=10, choices=BLOOD_TYPES)

    def __str__(self):
        return self.blood_type


class City(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hospital/')
    needed_blood_types = models.ManyToManyField(Blood)
    working_hours_start = models.TimeField()
    working_hours_end = models.TimeField()

    def __str__(self):
        return self.name


class RedCross(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='redcross/')
    working_hours_start = models.TimeField()
    working_hours_end = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.location}"



class Campaign(models.Model):

    CITY = [
        ('Skopje', 'Skopje'),
        ('Ohrid', 'Ohrid'),
        ('Bitola', 'Bitola'),
        ("Krushevo", "Krushevo"),
        ('Tetovo', 'Tetovo'),
        ('Kumanovo', 'Kumanovo'),
        ('Prilep', 'Prilep'),
    ]

    title = models.CharField(max_length=100)
    slogan = models.TextField(max_length=300, blank=True)
    description = models.TextField(max_length=300)
    organizer = models.CharField(max_length=200)
    city = models.CharField(max_length=50, choices=CITY)
    location = models.CharField(max_length=200)
    date_start = models.DateField()
    date_end = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    image = models.ImageField(upload_to='campaign/')
    featured = models.BooleanField(default=False)
    featured_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.organizer



class BloodDonor(models.Model):
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Donation(models.Model):
    donor = models.ForeignKey(BloodDonor, on_delete=models.CASCADE)
    date = models.DateField()
    blood_type = models.ForeignKey(Blood, on_delete=models.PROTECT)

    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, null=True, blank=True)
    red_cross = models.ForeignKey(RedCross, on_delete=models.PROTECT, null=True, blank=True)
    campaign = models.ForeignKey(Campaign,on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                        Q(hospital__isnull=False, red_cross__isnull=True, campaign__isnull=True)
                        | Q(hospital__isnull=True, red_cross__isnull=False, campaign__isnull=True)
                        | Q(hospital__isnull=True, red_cross__isnull=True, campaign__isnull=False)
                ),
                name='donation_has_exactly_one_location'
            )
        ]

    def __str__(self):
        return f"{self.donor} - {self.blood_type} - {self.date}"


class BloodStock(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_type = models.ForeignKey(Blood, on_delete=models.CASCADE)
    units_prefered_number = models.IntegerField()
    units_available = models.PositiveIntegerField()

    class Meta:
        unique_together = ('hospital', 'blood_type')

    def __str__(self):
        return f"{self.hospital} - {self.blood_type} - {self.units_available} - {self.units_prefered_number}"


class UrgentNeed(models.Model):
    URGENCY_CHOICES = [
        ('low', 'LOW'),
        ('critical', 'CRITICAL')
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_type = models.ForeignKey(Blood, on_delete=models.PROTECT)
    units_needed = models.PositiveIntegerField()
    blood_stock = models.ForeignKey(BloodStock, on_delete=models.PROTECT)
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hospital} - {self.blood_type}"


class ContactMessage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    attachment1 = models.FileField(upload_to='attachments/', blank=True, null=True)
    attachment2 = models.FileField(upload_to='attachments/', blank=True, null=True)
    attachment3 = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return self.title

