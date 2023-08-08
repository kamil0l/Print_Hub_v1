# w pliku forms.py
from django import forms
from .models import Filament, Printer, Parts, Project
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
                'first_name': 'Imię',
                'last_name': 'Nazwisko',
                'username': 'Login',
                  }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise ValidationError('hasła nie są takie same')
        return cleaned_data

class FilamentForm(forms.ModelForm):
    class Meta:
        model = Filament
        fields = ('name', 'producer', 'material', 'colour', 'temperature_min', 'temperature_max', 'weight')

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ('name', 'head', 'max_temperature', 'max_speed', 'image')

class PartsForm(forms.ModelForm):
    printers = forms.ModelMultipleChoiceField(
        queryset=Printer.objects.all(),  # Pobierz dostępne drukarki
        widget=forms.CheckboxSelectMultiple,  # Użyj checkboxów
        label="Przypisz do drukarki",
        required=False  # Nie wymagaj wyboru
    )

    class Meta:
        model = Parts
        fields = ['name', 'description', 'printers']

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'printer', 'material', 'filament_needed', 'print_time', 'image']
        labels = {
            'name': 'Nazwa',
            'printer': 'Drukarka',
            'material': 'Materiał',
            'filament_needed': 'Potrzebny filament (g)',
            'print_time': 'Czas wydruku (min)',
            'image': 'Zdjęcie',
        }
