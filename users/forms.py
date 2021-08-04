from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.http import HttpResponseRedirect
from django.shortcuts import render
from blog.models import Category


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def clean_email(self):
		data = self.cleaned_data['email']
		domain = data.split('@')[1]
		domain_list = ["somaiya.edu"]
		if domain not in domain_list:
			raise forms.ValidationError("Please enter an Email Address with a valid domain")
		try:
			match = User.objects.get(email=data)
		except User.DoesNotExist:
			return data    
		raise forms.ValidationError('This email address is already in use.')
		
		

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

	def clean_email(self):
		data = self.cleaned_data['email']
		domain = data.split('@')[1]
		domain_list = ["somaiya.edu"]
		if domain not in domain_list:
			raise forms.ValidationError("Please enter an Email Address with a valid domain")
		return data

	def save(self, commit=True):
		user = super(UserUpdateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

class ProfileUpdateForm(forms.ModelForm):
	# followed_category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),required=False,
    #                                     queryset=Category.objects.all())
	class Meta:
		model = Profile
		fields = ['college','about','followed_category']
		widgets = {
            'followed_category' : forms.CheckboxSelectMultiple,
        
        }
	
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['image'].widget.input_text = "Update image"
	# 	self.fields['image'].widget.initial_text = "Current image"


class ProfileImageUpdateForm(forms.ModelForm):
	image = forms.ImageField(label=('Profile Picture'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
	class Meta:
		model = Profile
		fields = ['image']
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['image'].widget.input_text = "Update image"
		self.fields['image'].widget.initial_text = "Current image"




class ProfileRegisterForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image','college', 'about', 'followed_category']
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['image'].widget.input_text = "Upload image"
		self.fields['image'].widget.initial_text = "Current image"
	