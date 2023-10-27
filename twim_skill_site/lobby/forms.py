from django import forms

class LobbyPasswordForm(forms.Form):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

