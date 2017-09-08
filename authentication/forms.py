from django import forms
from .models import User

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput,validators=[validate_password])
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','nikename','url')
        labels = {
            'email' : '邮箱',
            'url' : '网站(可选)'
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码不一致哦")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='密码',help_text='<a href="../password/">修改密码</a>')

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='邮箱',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput,validators=[validate_password])