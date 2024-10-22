from typing import Any
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from .models import Cliente, TipoTarjeta, Tarjeta

class RegistroUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

class CustomUserCreationForm(UserCreationForm):
    # Customizing the username field
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='awa de uwu',
        validators=[EmailValidator()],  # Example customization: enforce email format
        error_messages={
            'required': "Username is required.",
            'unique': "A user with that username already exists.",
        },
    )

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'genero', 'fecha_nacimiento', 'clave', 'correo', 'es_miembro']

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'clave': forms.PasswordInput(),
        }

class TipoTarjetaForm(forms.ModelForm):
    class Meta:
        model = TipoTarjeta
        fields = ['id_tipo', 'descripcion']


class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['numero_tarjeta', 'cvv', 'tipo', 'cliente']
        widgets = {
            'numero_tarjeta': forms.TextInput(attrs={'placeholder': 'Número de Tarjeta'}),
            'cvv': forms.TextInput(attrs={'placeholder': 'CVV'}),
        }