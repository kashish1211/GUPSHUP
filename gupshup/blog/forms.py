from django import forms
from .models import PostComment, Report

class NewCommentForm(forms.ModelForm):
	class Meta:
		model = PostComment
		fields = ['comment']

class NewReportForm(forms.ModelForm):
	class Meta:
		model = Report
		fields = []