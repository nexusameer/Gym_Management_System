from django import forms
from .models import *

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'


class ParticipantListForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['pname', 'id_card', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize how the form fields are displayed (optional)
        self.fields['pname'].widget.attrs.update({'class': 'custom-class'})
        self.fields['id_card'].widget.attrs.update({'class': 'custom-class'})
        # Add similar customizations for other fields if needed
        
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['participant', 'arrival_time', 'departure_time']

class MembershipPurchaseForm(forms.ModelForm):
    class Meta:
        model = MembershipPurchase
        fields = ['participant', 'membership_plan', 'start_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)