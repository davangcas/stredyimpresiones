from django.forms import ModelForm, TextInput, Textarea
from apps.administracion.models import *

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [
            'name',
            'link',
            'price',
        ]
        widgets = {
            'name':TextInput(
                attrs={
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
            'link':TextInput(
                attrs={
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
            'price':TextInput(
                attrs={
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
        }

class ImpresionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'on'
    
    class Meta:
        model = Impresion
        fields = [
            'hs',
            'mins',
            'grs',
            'speed',
            'infill',
            'material',
            'nozzle',
            'layer',
        ]
