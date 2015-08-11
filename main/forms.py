from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.models import User

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
                'placeholder': 'Contact character name (required)',
            }))

    # Override price widget to get bootstrap formatting
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Price (required)',
            }))

    # Override system from foreignkey to char (resolved in clean_system)
    system = forms.RegexField(
        regex=r'^J\d{6}$',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }))

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


class UserCreationForm(forms.ModelForm):
    '''
    A form that creates a user, with no priviledges, from the given username,
    email and password.
    '''
    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    username = forms.CharField(widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Username (kept private)',
                                   }))

    email = forms.CharField(validators=[EmailValidator],
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Email (kept private)',
                                }))

    password1 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Password',
                                    }))

    password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Password Verification',
                                    }))


    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
