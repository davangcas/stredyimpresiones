from django.forms import ModelForm, TextInput, Textarea
from apps.administracion.models import Cliente

class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'name':TextInput(
                attrs={
                    'class':'form-control',
                    'autocomplete':'off',
                }
            ),
            'phone':TextInput(
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
            'adress':TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Opcional',
                    'autocomplete':'off',
                }
            ),
        }