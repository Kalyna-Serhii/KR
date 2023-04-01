from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Ім\'я')
    last_name = forms.CharField(label='Прізвище')
    username = PhoneNumberField(
        label='Номер телефону',
        region="UA",
        widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'XX-XXX-XX-XX'}, initial='UA'),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')


class AuthenticationForm(AuthenticationForm):
    username = PhoneNumberField(
        label='Номер телефону',
        region="UA",
        widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'XX-XXX-XX-XX'}, initial='UA')
    )
