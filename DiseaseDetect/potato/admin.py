from django.contrib import admin
from .models import Remedies, HistImage, Feedback, Question, Answer,Tag, UserProfile
# Register your models here.

class RemediesAdmin(admin.ModelAdmin):
    list_display = ('disease','remedy_1','remedy_2','remedy_3','cause_1','cause_2','cause_3','symptom_1','symptom_2','symptom_3')
class HistImageAdmin(admin.ModelAdmin):
	list_display = ('img','result')
class FeedbackAdmin(admin.ModelAdmin):
    	list_display = ('email','feed')
class QuestionAdmin(admin.ModelAdmin):
    	list_display = ('title','ques','author','datetime',)

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('qid','uid','ans_body','datetime',)
class TagAdmin(admin.ModelAdmin):
	list_display=('tag',)

class UserProfileAdmin(admin.ModelAdmin):
	list_display=('user', 'avatar',)



admin.site.register(Remedies, RemediesAdmin)
admin.site.register(HistImage,HistImageAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(UserProfile,UserProfileAdmin)