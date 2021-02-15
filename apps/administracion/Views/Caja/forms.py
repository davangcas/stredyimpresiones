from django.forms import ModelForm, TextInput, Textarea
from apps.administracion.models import GastosMensuales, Extraccion, RegistroCaja

class GastosForm(ModelForm):
    class Meta:
        model = GastosMensuales
        fields = '__all__'
        widgets = {
            'name':TextInput(
                attrs={
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
            'cost':TextInput(
                attrs={
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
            'description':Textarea(
                attrs={
                    'class':'form-control',
                    'rows':'3',
                    'id':'textareaAutosize',
                    'placeholder':'Opcional',
                    'data-plugin-textarea-autosize':'',
                }
            ),
            'quantity':TextInput(
                attrs={
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
        }

class ExtraccionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = Extraccion
        fields = [
            'amount',
            'pay_user'
        ]

class RegistroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = RegistroCaja
        fields = [
            'concepto',
            'ingreso',
            'egreso',
            'pay_by',
        ]
