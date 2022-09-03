from django import forms
from .models import Logs, Policy, Rule


class PolicyCreateForm(forms.ModelForm):

    class Meta:
        model = Policy
        fields = ['name', 'logs', 'rule']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }


class PolicyUpdateForm(forms.ModelForm):

    class Meta:
        model = Policy
        fields = ['name', 'logs', 'rule']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }


class LogUpdateForm(forms.ModelForm):

    class Meta:
        model = Logs
        fields = ['file_path', 'event_type']
        widgets = {
            'file_path': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'event_type': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }


class RuleCreateForm(forms.ModelForm):

    class Meta:
        model = Rule
        fields = ['name', 'permission', 'accsess']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'permission': forms.Select(),
            'accsess': forms.Select(),
        }


class RuleUpdateForm(forms.ModelForm):

    class Meta:
        model = Rule
        fields = ['name', 'permission', 'accsess']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'permission': forms.Select(),
            'accsess': forms.Select(),
        }
