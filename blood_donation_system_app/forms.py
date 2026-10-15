from django import forms
from blood_donation_system_app.models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('title', 'description', 'email', 'phone_number', 'attachment1', 'attachment2', 'attachment3')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'attachment1': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment2': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment3': forms.FileInput(attrs={'class': 'form-control'}),
        }