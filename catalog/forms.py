from django import forms
from .models import Product, Version

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'unit_price']
    
    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 
                         'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Название не может содержать слово "{word}"')
        
        return cleaned_data
    
    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if cleaned_data:
            forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 
                             'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
            
            for word in forbidden_words:
                if word in cleaned_data.lower():
                    raise forms.ValidationError(f'Описание не может содержать слово "{word}"')
        
        return cleaned_data

class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current'] 