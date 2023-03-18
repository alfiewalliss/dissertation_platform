from django import forms
from .models import Comment, Post
from django_select2 import forms as s2forms
import datetime

class CommentForm(forms.ModelForm):
    body = forms.Textarea()

    class Meta:
        model = Comment
        fields = ['body']

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'autocomplete':'off',
        'id':'name',
    }))


class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000, widget=forms.TextInput(attrs={
        'autocomplete':'off',
        'placeholder': 'Message',
    }))

class PrimaryTagWiget(s2forms.ModelSelect2Widget):
    search_fields = [
        "tags__icontains",
    ]
    attrs = {'data-minimum-input-length': 1}

class SecondaryTagsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "tags__icontains",
    ]
    
class DateInput(forms.DateInput):
    input_type = 'date'


class PostForm(forms.ModelForm):
    publication_date = forms.DateField(widget=DateInput(attrs={'value': datetime.date.today()}), label="Date Published <small class='text-muted'>(Leave as todays date if this is the first publish or enter date of first publication at another journal if not) </small>")
    identifier = forms.URLField(label="DOI or Identifier <small class='text-muted'>(Leave empty to generate a new URL)</small>", required=False)
    version = forms.FloatField(widget=forms.NumberInput(attrs={'value': 1}))
    publisher = forms.CharField(widget=forms.TextInput(attrs={'value': 'Dissertation Exchange'}), label="Publisher <small class='text-muted'>(Leave as Dissertation Exchange unless paper has been published elsewhere)</small>")
    class Meta:
        model = Post
        fields = ('publisher', 'publication_date', 'identifier', 'version', 'title', 'abstract', 'file', 'primary_tag', 'secondary_tags')
        widgets = {
            'file': forms.FileInput(attrs={'accept':'application/pdf', 'id':'file'}),
            'primary_tag': PrimaryTagWiget(),
            'secondary_tags': SecondaryTagsWidget(),
        }



