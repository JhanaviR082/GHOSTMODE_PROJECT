from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import DailyCheckIn
from .models import ProductiveNote

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    dark_mode = forms.BooleanField(required=False, initial=False)
    ghost_avatar = forms.CharField(max_length=100, required=False, initial='ghost1.png')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'dark_mode', 'ghost_avatar')

class CheckInForm(forms.ModelForm):
    class Meta:
        model = DailyCheckIn # type: ignore
        fields = ['checked_in']
        widgets = {
            'checked_in': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'checked_in': 'I stayed off today'
        }
        
class ProductiveNoteForm(forms.ModelForm):
    class Meta:
        model = ProductiveNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'placeholder': 'What productive thing did you do today?', 'rows': 3}),
        }