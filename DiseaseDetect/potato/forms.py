from django import forms
from django.forms import ModelForm
from .models import Question, Answer, UserProfile, Remedies, Tag
from django.contrib.auth.models import User

class QuestionForm(forms.ModelForm):
	class Meta:
		model=Question
		fields = [
		'tag_id',
		'title',
		'ques',]

class AnswerForm(forms.ModelForm):
	class Meta:
 		model=Answer
 		fields=[
 		'ans_body']

class UserForm(forms.ModelForm):
	class Meta:
		model=User
		fields=[
		'username',
		'first_name',
		'last_name',
		'email']

		
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields=[
		'avatar']

class remedyForm(forms.ModelForm):
	class Meta:
		model=Remedies
		fields=[
		'disease',
		'remedy_1',
		'remedy_2',
		'remedy_3',
		'cause_1',
		'cause_2',
		'cause_3',
		'symptom_1',
		'symptom_2',
		'symptom_3']


class TagForm(forms.ModelForm):
    class Meta:
	    model=Tag
	    fields = ['tag']