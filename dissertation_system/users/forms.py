from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from blog.models import Tag
from django.forms import Textarea
from django_select2 import forms as s2forms

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=12, label="First Name")
    last_name = forms.CharField(max_length=12, label="Last Name")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class TagsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "tags__icontains",
    ]

class ProfileUpdateForm(forms.ModelForm):
    #tags = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple, queryset=Tag.objects.all())
    class Meta:
        model = Profile
        fields = ['bio', 'image', 'tags']
        widgets = {
            'bio': Textarea(attrs={'rows':5}),
            'tags': TagsWidget(),
        }
        