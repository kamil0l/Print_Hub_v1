# w pliku forms.py
from django import forms
from .models import Filament, Printer, Parts, Project

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
