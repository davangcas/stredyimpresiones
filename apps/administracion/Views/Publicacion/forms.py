from django.forms import ModelForm, Select

from apps.principal.models.publication import Publication

class PublicacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'on'

    class Meta:
        model = Publication
        fields = [
            'title',
            'product',
            'image',
            'detail',
        ]
        widgets = {
            'product':Select(
                attrs={
                    'class':'form-control',
                    'data-plugin-selectTwo':'',
                }
            )
        }
