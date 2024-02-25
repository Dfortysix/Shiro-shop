from django import forms
from .models import Order

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1',
                  'address_line_2', 'country', 'city', 'order_note']
        widgets = {

            'firstname': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'lastname': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'phone': forms.NumberInput(attrs={
                'class': INPUT_CLASSES
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES
            }),
            'country': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'city': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'address_line_1': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'address_line_2': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'order_note': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            })
        }
