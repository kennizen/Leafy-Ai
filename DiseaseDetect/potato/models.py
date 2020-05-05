from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Remedies(models.Model):
	disease = models.CharField(max_length=256)
	remedy_1 = models.TextField()
	remedy_2 = models.TextField()
	remedy_3 = models.TextField()
	cause_1 = models.TextField()
	cause_2 = models.TextField()
	cause_3 = models.TextField()
	symptom_1 =models.TextField()
	symptom_2 = models.TextField()
	symptom_3 = models.TextField()

	class Meta:
		verbose_name_plural = 'Remedies'


class HistImage(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	img = models.ImageField(upload_to='media/')
	result = models.CharField(max_length=256)


class Feedback(models.Model):
	email = models.CharField(max_length=256)
	feed = models.TextField()


class Tag(models.Model):
	tag = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.tag


class Question(models.Model):
	tag_id=models.ForeignKey(Tag,to_field='tag',on_delete=models.CASCADE)
	title=models.CharField(max_length=1000)
	ques=RichTextUploadingField(blank = False, null = False)
	author=models.ForeignKey(User, on_delete=models.CASCADE)
	datetime= models.DateTimeField(default=timezone.now)

	def _str_(self):
    		return '%s' % (self.id)


class Answer(models.Model):
	qid=models.ForeignKey(Question,on_delete=models.CASCADE)
	uid=models.ForeignKey(User,on_delete=models.CASCADE)
	ans_body=RichTextUploadingField()
	datetime=models.DateTimeField(default=timezone.now)
	

class UserProfile(models.Model):
	user   = models.OneToOneField(User, on_delete = models.CASCADE)
	avatar = models.ImageField(upload_to='media/')
	is_expert = models.BooleanField(default=False) 