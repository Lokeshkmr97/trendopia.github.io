from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer,contact

class CustomerRegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete": "current-password",'class':'form-control'})
    )

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "autofocus": True,'class':'form-control'}),)

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control'}),
    )

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email",'class':'form-control'}),
    )

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control'}),
    )

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','state','zipcode']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'locality':forms.TextInput(attrs={'class':'form-control'}),
                 'city':forms.TextInput(attrs={'class':'form-control'}),
                 'state':forms.Select(attrs={'class':'form-control'}),
                 'zipcode':forms.NumberInput(attrs={'class':'form-control'})}
        
class ContactForm(forms.ModelForm):
    class Meta:
        model=contact
        fields=['fullname','email','mobile','comment']
        labels={'email':'Email ID','fullname':'Full Name'}
        widgets={
            'fullname':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'comment':forms.Textarea(attrs={'class':'form-control','rows':4, 'cols':15}),
        }
        