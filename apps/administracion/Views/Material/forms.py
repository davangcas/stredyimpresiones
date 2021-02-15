from django.forms import ModelForm, TextInput
from apps.administracion.models import Material, PlasticoDisponible

class MaterialForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = Material
        fields = '__all__'

class ColorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = PlasticoDisponible
        fields = '__all__'
        widgets = {
            'available':TextInput(
                attrs={
                    'placeholder':'1000 gramos por defecto',
                }
            ),
        }
