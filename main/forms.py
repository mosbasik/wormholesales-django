from django import forms

from main.models import Order, System


class OrderModelForm(forms.ModelForm):

    system = forms.RegexField(regex=r'^J\d{6}$', required=True)
    error_css_class = 'has-error'
    required_css_class = 'has-error'

    class Meta:
        model = Order
        fields = '__all__'

    def clean_system(self):
        data = self.cleaned_data['system']
        if not System.objects.filter(j_code=data).exists():
            raise forms.ValidationError('Invalid J-Code!')
        else:
            data = System.objects.get(j_code=data)
            return data

    # def clean(self):
    #     cleaned_data = super(OrderModelForm, self).clean()
    #     import pprint
    #     print type(self.data)
    #     pprint.pprint(self.data)
    #     print type(cleaned_data)
    #     pprint.pprint(cleaned_data)
