from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.models import User

from main.models import Order, System, Character

from lxml import etree
import requests
import urllib


class OrderModelForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ['user']

    # Override contact_name widget to get bootstrap formatting
    contact_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contact character name (required)',
            }))

    # Override system from foreignkey to char (resolved in clean_system)
    system = forms.RegexField(
        regex=r'^J\d{6}$',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Wormhole J-code (required)',
            }))

    # Override price widget to get bootstrap formatting
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Price (required)',
            }))

    # Override information widget to get textarea and bootstrap formatting
    information = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Information',
                'rows': '10',
            }))

    # TODO
    # error_css_class = 'has-error'
    # required_css_class = 'has-error'

    def clean_contact_name(self):
        '''
        Gets the contact name from the form data and checks to see if that
        character exists through Eve's character API. If it exists, that
        Character object is returned (changing the type from a string to an
        object to support the foreign key in Order); otherwise raises a
        ValidationError.
        '''
        name = self.cleaned_data['contact_name']

        # if name is already in our database, it's VALID
        if Character.objects.filter(name=name).exists():

            # return the Character object with that name
            # (NOTE: this changes the type from a string to a Character!)
            return Character.objects.filter(name=name)

        # if name is not already cached in our database, check the API
        else:
            url_stub = 'https://api.eveonline.com/eve/CharacterID.xml.aspx?names='
            response = requests.get(url_stub + name)
            tree = etree.XML(response.content)
            character_id_xpath = '/eveapi/result/rowset/row/@characterID'
            character_id = int(tree.xpath(character_id_xpath)[0])

            # if the API returns an id of 0, name is INVALID; raise an error
            if character_id == 0:
                raise forms.ValidationError('Character does not exist.')

            # otherwise the name is VALID; create corresponding character
            name = Character.objects.create(id=character_id, name=name)

            # return Character object
            # (NOTE: this changes the type from a string to a Character!)
            return name

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
