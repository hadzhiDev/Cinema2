from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login_input',
        'placeholder': 'Enter username'}), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login_input ',
        'placeholder': 'Enter password',
        'required': True}))

