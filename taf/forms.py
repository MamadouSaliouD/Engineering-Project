from django import forms
from .models import User, Task
import pycountry
from django.contrib.auth import password_validation



class UserCreationForm(forms.ModelForm):
    COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=False, help_text="Please select an area code")
    city = forms.CharField(max_length=64)
    #created_time = forms.DateTimeField(auto_now_add=True)
    name = forms.CharField(max_length=64)
    surname = forms.CharField(max_length=64)
    username = forms.CharField(max_length=64)

    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'country', 'city']


    def clean_password2(self):
        password2 = super().clean_password2()
        username = self.cleaned_data.get('username')
  
        if username and password2 and password2 in username:
           raise forms.ValidationError(
                                self.error_messages['password_similar_username'],
                                code='password_similar_username',
                                )
  
           password_validation.validate_password(password2, self.instance)
  
        return password2



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'start_time', 'end_time']