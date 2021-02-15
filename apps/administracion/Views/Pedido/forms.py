from django.forms import ModelForm, Select

from apps.administracion.models import *

class PedidoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control populate'
            form.field.widget.attrs['autocomplete'] = 'on'
    
    class Meta:
        model = Pedido
        fields = ['cliente',]
        widgets = {
            'cliente':Select(
                attrs={
                    'data-plugin-selectTwo':'',
                }
            )
        }

class DetallePedidoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'on'

    class Meta:
        model = DetallePedido
        fields = [
            'producto',
            'cantidad',
        ]
        widgets = {
            'producto':Select(
                attrs={
                    'class':'form-control',
                    'data-plugin-selectTwo':'',
                }
            )
        }

class ImpresionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'on'
    
    class Meta:
        model = ImpresionPedido
        fields = [
            'color',
        ]
