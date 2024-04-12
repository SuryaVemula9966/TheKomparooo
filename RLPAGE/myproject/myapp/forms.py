# forms.py
import re
from django import forms
from .models import Register

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Register
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if " " in username:
            raise forms.ValidationError("Username cannot contain spaces.")
        
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
            raise forms.ValidationError("Username can only contain alphabets, numbers, and underscores, and must start with an alphabet.")
        
        if len(username) > 20:
            raise forms.ValidationError("Username must be 20 characters or fewer.")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if " " in password:
            raise forms.ValidationError("Password cannot contain spaces.")
        
        # Check if password starts with an alphabet
        if not password[0].isalpha():
            raise forms.ValidationError("Password must start with an alphabet.")

        # Check if password contains only allowed characters
        if not re.match(r'^[a-zA-Z0-9_@#$]+$', password):
            raise forms.ValidationError("Password can only contain alphabets, numbers, and special characters @_#$.")

        return password
   
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")

        if " " in confirm_password:
            raise forms.ValidationError("Confirm password cannot contain spaces.")

        if confirm_password != self.cleaned_data.get("password"):
            raise forms.ValidationError("Passwords do not match.")

        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if " " in email:
            raise forms.ValidationError("Email cannot contain spaces.")

        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Email must end with @gmail.com.")

        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number")

        if mobile_number is not None and mobile_number.strip() == "":
            return None  # Return None if mobile_number is empty
        
        # Check if mobile number contains only digits and has exactly 10 digits
        if not re.match(r'^\d{10}$', mobile_number):
            raise forms.ValidationError("Mobile number must contain exactly 10 digits and only digits are allowed.")

        return mobile_number
