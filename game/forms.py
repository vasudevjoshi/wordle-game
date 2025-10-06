from django import forms
from django.contrib.auth.models import User
import re

USERNAME_RE = re.compile(r'^[A-Za-z]{5,}$')  # only letters, ≥5
PASSWORD_RE = re.compile(r'^(?=.{5,}$)(?=.*[A-Za-z])(?=.*\d)(?=.*[$%*@]).*$')

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_username(self):
        u = self.cleaned_data['username']
        if not USERNAME_RE.match(u):
            raise forms.ValidationError('Username must be at least 5 letters (A-Z or a-z).')
        if User.objects.filter(username=u).exists():
            raise forms.ValidationError('Username already exists.')
        return u

    def clean_password(self):
        p = self.cleaned_data['password']
        if not PASSWORD_RE.match(p):
            raise forms.ValidationError('Password must have ≥5 chars, 1 letter, 1 number & 1 of $%*@.')
        return p

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned
