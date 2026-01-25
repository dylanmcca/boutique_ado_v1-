from django import forms
from django_countries.fields import CountryField
from .models import Order


class OrderForm(forms.ModelForm):
    # Override the country field with a regular ChoiceField
    # to avoid crispy_forms rendering issues with BlankChoiceIterator
    country = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select d-block', 'required': 'required'}),
    )
    
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        
        # Get the country choices from the model field and materialize them
        country_field = Order._meta.get_field('country')
        self.fields['country'].choices = [('', 'Country *')] + list(country_field.choices)
        
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
        
        # Add styling to make country placeholder appear disabled/greyed out
        self.fields['country'].widget.attrs['class'] = 'stripe-style-input'