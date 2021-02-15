from django.forms import ModelForm
from apps.administracion.models import Datos

class DatosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'on'

    class Meta:
        model = Datos
        fields = '__all__'
        