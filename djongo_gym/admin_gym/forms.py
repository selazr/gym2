from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminUserCreationForm(forms.ModelForm):
    """Formulario para que los administradores registren nuevos usuarios"""
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AdminUserUpdateForm(forms.ModelForm):
    """Formulario para que los administradores editen usuarios y asignen roles"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']
