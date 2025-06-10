from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Rutina
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    """Formulario para que el usuario pueda actualizar sus datos."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulario para cambiar la contraseña, asegurando que la nueva sea diferente a la actual."""

    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_new_password1(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")
        if old_password and new_password1 and old_password == new_password1:
            raise forms.ValidationError("La nueva contraseña no puede ser igual a la actual.")
        return new_password1
    
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class SimpleRutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la rutina'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la rutina'
            })
        }

        def clean_name(self):
            name = self.cleaned_data['name']
            if len(name) < 3:
                raise forms.ValidationError("El nombre ha de tener al menos tres caracteres")
            return name