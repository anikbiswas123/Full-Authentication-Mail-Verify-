from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from Accounts.models import User



class UserCreationForm(forms.ModelForm):
    """
    নতুন ব্যবহারকারী তৈরি করার জন্য একটি ফর্ম এর ভেটর সমস্ত প্রয়োজনীয় তথ্য অন্তর্ভুক্ত করা যায়
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "mobile", "address", "is_customer", "is_seller"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "mobile", "address", "is_active", "is_admin", "is_customer", "is_seller"]

    def clean_password(self):
        return self.initial['password']


