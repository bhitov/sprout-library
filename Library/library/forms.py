from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from library.models import Book

class BookForm(forms.ModelForm):
    image_link = forms.CharField(max_length = 150)
    author = forms.CharField(max_length = 50)
    title = forms.CharField(max_length = 250)
    barcode = forms.CharField(max_length = 20)
    
    class Meta:
        model = Book
        fields = ('image_link','author','title','barcode',)

class UserForm(forms.Form):
    username = forms.CharField(max_length = 30)
    first_name = forms.CharField(max_length = 30)
    last_name = forms.CharField(max_length = 30)
    email = forms.EmailField()
    password = forms.CharField(max_length = 20, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length = 20, widget=forms.PasswordInput)
    
    def clean_password(self):
        p = self.data.get('password','')
        p_con = self.data.get('password_confirmation','')
        if p != p_con:
            raise forms.ValidationError
        return p
    
    def save(self, force_insert=False, force_update=False, commit=True):
        data = self.data
        user = User.objects.create_user(data['username'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']

class BookSearch(forms.Form):
    barcode = forms.CharField(max_length = 40)
        

    