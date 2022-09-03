from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name']
        widgets = {
           'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
           'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
           'email': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
           'username': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }

class ChangeUserPasswordForm(PasswordChangeForm):
    old_password = forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'fasdfuser'})
    new_password1 = forms.PasswordInput(attrs={'class': 'form-control form-control-user'})
    new_password2 = forms.PasswordInput(attrs={'class': 'form-control form-control-user'})


class EditUserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'is_superuser']
        widgets = {
           'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
           'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
           'email': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
           'username': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }