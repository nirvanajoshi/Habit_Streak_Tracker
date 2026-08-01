from django import forms
from .models import Habit, CheckIn, Partnership

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'frequency']
        
class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['date', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class PartnershipForm(forms.ModelForm):
    class Meta:
        model = Partnership
        fields = [ 'partner']
        widgets = {
            'partner': forms.Select(attrs={'class': 'form-control'}),
        }

