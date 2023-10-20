from django import forms

from newsletter.models import Newsletter, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductsForm(StyleFormMixin, forms.ModelForm):
    exceptional_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
    
    class Meta:
        model = Products
        exclude = ('created_at', 'updated_at', 'user')

    def clean_product_name(self):
        cleaned_data = self.cleaned_data.get('product_name')
        self.check_exceptional_words(self.exceptional_words, cleaned_data)
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        self.check_exceptional_words(self.exceptional_words, cleaned_data)
        return cleaned_data

    @staticmethod
    def check_exceptional_words(exceptional_words, cleaned_data):
        for word in exceptional_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Нельзя использовать слово {word}!')


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
