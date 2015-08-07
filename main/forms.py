from django import forms

from main.models import Order, System


class OrderModelForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

    # Override contact_name widget to get bootstrap formatting
    contact_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contact character name',
            }
        )
    )

    # Override price widget to get bootstrap formatting
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Price',
            }
        )
    )

    # Override system from foreignkey to char (resolved in clean_system)
    system = forms.RegexField(
        regex=r'^J\d{6}$',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Price',
            }
        )
    )

    # TODO
    # error_css_class = 'has-error'
    # required_css_class = 'has-error'

    def clean_system(self):
        '''
        Gets the J-code string from the form data, checks to see if a system
        with that J-code exists, and if it does, replaces the string with the
        corresponding System object.  Otherwise raises a ValidationError.
        '''
        data = self.cleaned_data['system']
        if not System.objects.filter(j_code=data).exists():
            raise forms.ValidationError('Invalid J-code.')
        else:
            data = System.objects.get(j_code=data)
            return data

    def clean_price(self):
        '''
        Gets the price string from the form data, removes commas and casts the
        result to a float.  If this fails, raises a ValidationError.
        '''
        data = self.cleaned_data['price']
        try:
            data = float(data.replace(',', ''))
            return data
        except ValueError, e:
            raise forms.ValidationError('Invalid price.')
