from django import forms
from .models import PostComment

class NewCommentForm(forms.ModelForm):
	class Meta:
		model = PostComment
		fields = ['content']