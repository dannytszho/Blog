from django import forms

from .models import BlogPost, Entry

class BlogPostForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ['text','public']
		labels = {'text': '', 'public':'Make it public?'}

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['text']
		labels = {'text':''}
		widgets = {'text': forms.Textarea(attrs={'cols':80})}
