from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from tempfacetrace.models import Student, Attendance, ImageDetails

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address.")
    domain = forms.CharField(max_length=50)
    studentid = forms.IntegerField()
    studentname = forms.CharField(max_length=50, help_text="Required. Enter your Name.")

    class Meta:
        model = Student
        fields = ('email', 'studentname', 'domain', 'studentid', 'password1', 'password2',)

        def clean_email(self):
            email = self.cleaned_data['email'].lower()
            try:
                student = Student.objects.exclude(pk = self.instance.pk).get(email=email)
            except Student.DoesNotExist:
                return email
            raise forms.ValidationError(f'Email {email} is already in use.')
        
        def clean_studentid(self):
            studentid = self.cleaned_data['studentid']
            try:
                student = Student.objects.exclude(pk = self.instance.pk).get(studentid = studentid)
            except Student.DoesNotExist:
                return studentid
            raise forms.ValidationError(f'{studentid} is already registered.')
        

        
class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Student
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")
                  


class ImageDetailsUploadForm(forms.ModelForm):
      class Meta:
            model = ImageDetails
            fields = '__all__'  
                    