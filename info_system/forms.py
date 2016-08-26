from models import Student, Manager, SCHOOL
from django import forms


class StudentForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100, 
                                 widget=forms.TextInput({"placeholder": "Jack"}))
    middle_name = forms.CharField(label='Middle Name', max_length=100,
                                  widget=forms.TextInput({"placeholder": "Kofi"}))
    surname = forms.CharField(label='Surname', max_length=100,
                                  widget=forms.TextInput({"placeholder": "Eboyomi"}))
    id_number = forms.CharField(label='ID Number', max_length=20,
                                  widget=forms.TextInput({"placeholder": "ABS15A00234Y"}))
    phone_number = forms.CharField(label='Phone Number', max_length=20,
                                  widget=forms.TextInput({"placeholder": "+233241234567"}))
    email_address = forms.EmailField(label="Email", max_length=50, 
                                  widget=forms.EmailInput({"placeholder": "example@yahoo.com"}))
    password = forms.CharField(widget=forms.PasswordInput({"placeholder": "Enter a password"}), 
                                  label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput({"placeholder": "Repeat password"}),
                                  label="Confirm Password")
    program = forms.ChoiceField(widget=forms.RadioSelect, choices=SCHOOL)


class StudentLoginForm(forms.Form):
    id_number = forms.CharField(label='ID Number', max_length=20,
                                  widget=forms.TextInput({"placeholder": "ABS15A00234Y"}))
    password  = forms.CharField(widget=forms.PasswordInput({"placeholder": "Enter your password"}), 
                                  label="Password")

class ManagerForm(forms.Form):
    first_name = forms.CharField(label='First Name',max_length=100)
    middle_name = forms.CharField(label='Middle Name', max_length=100)
    surname = forms.CharField(label='Surname',max_length=100) 


class AdminLoginForm(forms.Form):
    username  = forms.CharField(label='Username', max_length=30,
                                  widget=forms.TextInput({"placeholder": "Enter your Username"}))
    password  = forms.CharField(widget=forms.PasswordInput({"placeholder": "Enter your Password"}), 
                                  label="Password")

class PasswordResetRequestForm(forms.Form):
    email_address = forms.EmailField(label="Email", max_length=50, 
                                  widget=forms.EmailInput({"placeholder": "example@yahoo.com"}))


class PasswordResetConfirmForm(forms.Form):
    password  = forms.CharField(widget=forms.PasswordInput({"placeholder": "Enter Password"}), 
                                  label="Password")
    password_confirm  = forms.CharField(widget=forms.PasswordInput({"placeholder": "Repeat Password"}), 
                                  label="Confirm Password")
    def clean(self):
        if (self.cleaned_data.get('password'))!= (self.cleaned_data.get('password_confirm')):
            raise forms.ValidationError("Passwords provided do not match")
        return self.cleaned_data
            
