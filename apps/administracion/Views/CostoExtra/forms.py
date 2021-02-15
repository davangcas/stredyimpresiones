from django.forms import ModelForm

from apps.administracion.models import CostoExtra

class CostoExtraForm(ModelForm):
    class Meta:
        model = CostoExtra
        fields = [
            'concept',
            'amount',
        ]
