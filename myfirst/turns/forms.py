from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import AuthenticationForm
from turns.models import Turn

User = get_user_model()


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Ім\'я')
    last_name = forms.CharField(label='Прізвище')
    username = PhoneNumberField(
        label='Номер телефону',
        region='UA',
        widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'XX-XXX-XX-XX'}, initial='UA'))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')


class AuthenticationForm(AuthenticationForm):
    username = PhoneNumberField(
        label='Номер телефону',
        region='UA',
        widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'XX-XXX-XX-XX'}, initial='UA'))


class TurnForm(ModelForm):
    class Meta:
        model = Turn
        fields = ['turn_title', 'turn_text']
        widgets = {
            'turn_title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва',
                'name': 'turn_title'
            }),
            'turn_text': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Опис',
                'name': 'turn_text'
            }),
        }
