from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    # Override the country field to avoid crispy_forms rendering issues
    default_country = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select d-block'}),
    )
    
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        
        # Get the country choices from the model field and materialize them
        country_field = UserProfile._meta.get_field('default_country')
        self.fields['default_country'].choices = [
            ('', 'Country')
        ] + list(country_field.choices)
        
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = (
                'border-black rounded-0 profile-form-input'
            )
            self.fields[field].label = False