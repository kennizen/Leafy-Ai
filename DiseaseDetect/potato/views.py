from django.http import HttpResponse
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from diseaseDetection.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


### Machile Learning Imports ###
# from . models import Remedies, HistImage, Feedback
# from keras.preprocessing import image
# from keras.models import load_model
# from removebg import RemoveBg
# import random, string
# import numpy as np
# import tensorflow as tf
# import base64
### Machile Learning Imports ###

###Dialogflow Webhook imports###
import os
from django.http import JsonResponse
import json
import dialogflow
from google.api_core.exceptions import InvalidArgument
###Dialogflow Webhook imports###

###Database imports###
from . models import Remedies, HistImage, Question, Answer, Tag, UserProfile, Feedback
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login
from django.db.models import Count
###Database imports###

###Django Template Render Imports###
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm, UserForm, UserProfileForm, remedyForm, TagForm
from django.core.paginator import Paginator
###Django Template Render Imports###


# graph = tf.get_default_graph()

# path = os.path.join(settings.MODELS, 'Own_Model.h5')
# Detector = load_model(path)

# def prediict(img):

#     img = image.load_img(img, target_size=(224, 224))
#     img_tensor = image.img_to_array(img)  # Image data encoded as integers in the 0–255 range
#     img_tensor = np.expand_dims(img_tensor, axis = 0)
#     with graph.as_default():
#         prediction = Detector.predict(img_tensor)
#         classes = ["Cherry Powdery mildew","Corn common rust","Corn healthy","Corn Northern leaf blight","Potato Early Blight","Potato Healthy",
#         "Potato Late blight","Squash Powdery mildew","Tomato Healthy","Tomato Late blight","Tomato Yellow Leaf Curl Virus"]

#         result = str(classes[np.argmax(np.array(prediction[0]))])
#         return result


# Create your views here.
def main(request):
    context = {'title': 'Home Page'}
    return render(request, 'main.html', context)


def info(request):
    return render(request, 'info.html', {'title': 'Information'})


def feedback(request):
    if request.method == "POST":
        email = request.POST['email']
        feedback = request.POST['feedback']

        feed = Feedback(email=email, feed=feedback)

        feed.save()

        # subject = 'Feedback'
        # message = 'Thank you for your feedback. Team-Leafy'
        # send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently = False)

        return render(request, 'feedSubmitted.html')

    return render(request, 'feedback.html')


def index(request):
    if(request.method == 'GET'):
        if request.user.is_anonymous:
            context = {'title': 'Detection'}
            return render(request, 'index.html', context)
        else:
            history = HistImage.objects.all().filter(
                user=request.user).order_by('id').reverse()
            args = {}
            args['history'] = history
            args['title'] = 'Detection'
            return render(request, 'index.html', args)
    else:
        imag = request.FILES.get('pic')

        b64_image = base64.b64encode(imag.file.read()).decode('ascii')

        # stringLength=10
        # letters = string.ascii_lowercase
        # file_name = ''.join(random.choice(letters) for i in range(stringLength))

        # rmbg = RemoveBg("nhahVkAMQTPACG5Z8NiEuWxs", "error.log")
        # rmbg.remove_background_from_base64_img(b64_image, file_name)

        # noImgPath = os.path.join(settings.BASE_DIR, file_name)
        # with open(noImgPath, "rb") as image_file:
        #     b64_image_new = base64.b64encode(image_file.read()).decode('ascii')

        prediction = prediict(imag)
        remedy = Remedies.objects.all().filter(disease=prediction)

        if request.user.is_anonymous:
            args = {}
            args['disease'] = prediction
            args['image'] = b64_image
            args['remedy'] = remedy
        else:
            history = HistImage(user=request.user, img=imag, result=prediction)
            history.save()
            history = HistImage.objects.all().filter(
                user=request.user).order_by('id').reverse()

            args = {}
            args['disease'] = prediction
            args['image'] = b64_image
            args['remedy'] = remedy
            args['history'] = history
            args['title'] = 'Detection'
            # args['image_2'] = b64_image_new

        return render(request, 'index.html', args)

def chat(request):
    if request.method=="GET":
        return render(request,'chatabot.html')
    else:
        #DIALOGFLOW_PROJECT_ID = 'chatbot-kovqhd'
        DIALOGFLOW_PROJECT_ID ='chatbot-kovqhd'
        DIALOGFLOW_LANGUAGE_CODE = 'en-US'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'E:/code/6th Sem/DiseaseDetect/chatbot-kovqhd-787be5a40d48.json'
        SESSION_ID = 'abcd12'
        

        text_to_be_analyzed = request.POST.get('query')
        print(text_to_be_analyzed)
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise

        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
        
        reply=response.query_result.fulfillment_text
        data={
        'replyy':reply
        }
        return JsonResponse(data)

def fullResult(request, result):
    rem = Remedies.objects.all().filter(disease=result)
    # hist = HistImage.objects.all().filter(id=result)
    return render(request, 'fullResult.html', {'rem': rem})

# First page of faq, renders questions and user related info


def faq(request):
    if request.method == "GET":
        profileImage = UserProfile.objects.all()
        questions = Question.objects.annotate(
            num_ans=Count('answer')).order_by('datetime').reverse()
        paginator = Paginator(questions, 10)  # Show 25 contacts per page.
        num_qs = Question.objects.count()

        if request.user.is_anonymous:
            num_pos = 0
            avatar = None
        else:
            num_pos = Question.objects.filter(author=request.user).count()
            avatar = UserProfile.objects.filter(user=request.user)
        print(num_qs)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        tags = Tag.objects.all()
        context = {'title': 'QnA', 'tags': tags, 'page_obj': page_obj, 'user': request.user,
                   'num_qs': num_qs, 'num_pos': num_pos, 'avatar': avatar, 'profileImage': profileImage}
        return render(request, 'faqHome.html', context)
    else:
        profileImage = UserProfile.objects.all()
        tag = request.POST.get('tags')
        if tag == 'show all':
            questions = Question.objects.annotate(
                num_ans=Count('answer')).order_by('datetime').reverse()
        else:
            questions = Question.objects.annotate(num_ans=Count('answer')).order_by(
                'datetime').reverse().filter(tag_id=tag)
        paginator = Paginator(questions, 10)  # Show contacts per page.
        if tag == 'show all':
            num_qs = Question.objects.count()
        else:
            num_qs = Question.objects.filter(tag_id=tag).count()

        if request.user.is_anonymous:
            num_pos = 0
            avatar = None
        else:
            num_pos = Question.objects.filter(author=request.user).count()
            avatar = UserProfile.objects.filter(user=request.user)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        tags = Tag.objects.all()
        context = {'title': 'QnA', 'tags': tags, 'page_obj': page_obj, 'user': request.user,
                   'num_qs': num_qs, 'num_pos': num_pos, 'avatar': avatar, 'profileImage': profileImage}
        return render(request, 'faqHome.html', context)


# Allows user to post a new question only when logged in
@login_required(login_url='/login/')
def postqn(request):
    if request.method == "GET":
        form = QuestionForm()
        context = {'title': 'Post questions', 'form': form}
        return render(request, 'askquestion.html', context)
    else:
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
        return redirect(faq)


# fetches the answers to the question clicked on main faq page
def getans(request, id):
    answers = Answer.objects.all().filter(qid=id).order_by('datetime').reverse()
    print(answers)
    avatar = UserProfile.objects.all()
    questions = Question.objects.all().filter(id=id)
    return render(request, 'answer.html', {'ans': answers, 'ques': questions, 'id': id, 'title': 'Answers', 'avatar': avatar})


# Allows user to post a new answer only when logged in
@login_required(login_url='/login/')
def postans(request, id):
    if request.method == "GET":
        form = AnswerForm()
        avatar = UserProfile.objects.all()
        question = Question.objects.filter(id=id)
        print(question)
        context = {'title': 'Post answers', 'form': form,
                   'id': id, 'question': question, 'avatar': avatar}
        return render(request, 'postanswer.html', context)
    else:
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uid = request.user
            obj.qid = Question.objects.get(id=id)
            obj.save()
        return redirect(getans, id=id)


# login for user
def loginUser(request):
    if request.method == "GET":
        context = {'title': 'Login page'}
        return render(request, 'login.html', context)
    else:
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        user = authenticate(username=uname, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if request.POST.get('remember_me'):
                request.session.set_expiry(60*60*24*7)
                print('remembered')
            else:
                request.session.set_expiry(0)
                print('not remembered')
            print('User authenticated')
            print(request.POST.get('next'))
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            elif user.is_staff:
                return redirect(aadmin)
            else:
                return redirect(main)

        elif User.objects.filter(username=uname).exists():
            u = User.objects.get(username=uname)
            if u.check_password(password):
                if u.is_active == False:
                    print('entered if')
                    return render(request, 'block.html')

        return render(request, 'login.html', {'message1': 'No account with the above credentials was found.', 'message2': 'Username and password are case sensitive.', 'title': 'Login page'})


# Logout for user
def logoutUser(request):
    logout(request)
    return render(request, 'logout.html', {'title': 'logout'})


# unique user registration
def reg(request):
    if request.method == "GET":
        context = {'title': 'Sign up page'}
        return render(request, 'signUp.html', context)
    else:
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        print(uname)
        print(email)
        if User.objects.filter(username=uname).exists():
            umessage = "Username " + '"' + uname + '"' + " already exists"
            print(umessage)
            return render(request, 'signUp.html', {'umessage': umessage, 'title': 'Sign up page'})
        elif User.objects.filter(email=email).exists():
            emessage = '"' + email + '"' + " already exixts"
            print(emessage)
            return render(request, 'signUp.html', {'emessage': emessage, 'title': 'Sign up page'})
        else:
            password = request.POST.get('password1')
            email = request.POST.get('email')
            imag = request.FILES.get('pic')
            user = User.objects.create_user(uname)
            user.set_password(password)
            user.email = email
            user.save()
            Profile = UserProfile(user=user, avatar=imag)
            Profile.save()
            print('User created')
            context = {'title': 'Login page'}
            return render(request, 'login.html', context)


# shows user profile to display questions and answers given by user ONLY for logged in user
@login_required(login_url='/login/')
def profile(request):
    ulog = User.objects.all().filter(username=request.user)
    questions = Question.objects.all().filter(author=request.user)
    answers = Answer.objects.all().filter(uid=request.user)
    num_qs = Question.objects.filter(author=request.user).count()
    num_ans = Answer.objects.filter(uid=request.user).count()
    avatar = UserProfile.objects.filter(user=request.user)
    context = {
        'ulog': ulog,
        'questions': questions,
        'answers': answers,
        'num_qs': num_qs,
        'num_ans': num_ans,
        'avatar': avatar,
        'title': 'Your profile'
    }
    return render(request, 'profile.html', context)


# Shows the option to edit question for current user
def editqn(request, id):
    if request.method == "GET":
        u = Question.objects.get(id=id)
        form = QuestionForm(instance=u)  # No request.POST
        return render(request, 'editqn.html', {'form': form, 'u': id, 'title': 'Edit question'})
    else:
        instance = Question.objects.get(id=id)
        form = QuestionForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(faq)


def editans(request, id):
    if request.method == "GET":
        u = Answer.objects.get(id=id)
        print(u)
        form = AnswerForm(instance=u)
        avatar = UserProfile.objects.all()
        qid = Answer.objects.values_list('qid', flat=True).get(id=id)
        question = Question.objects.all().filter(id=qid)
        return render(request, 'editans.html', {'form': form, 'u': id, 'title': 'Edit answer', 'question': question, 'avatar': avatar})
    else:
        instance = Answer.objects.get(id=id)
        form = AnswerForm(request.POST or None, instance=instance)
        qid = Answer.objects.values_list('qid', flat=True).get(id=id)
        if form.is_valid():
            form.save()
            return redirect(getans, id=qid)


def deleteqn(request, id):
    if request.POST.get('yes') == 'yes':
        instance = Question.objects.filter(id=id).delete()

    return redirect(faq)


def deleteans(request, id):
    if request.method == "GET":
        return render(request, 'ansDeleteConfirm.html', {'id': id})
    else:
        if request.POST.get('yes') == 'yes':
            qid = Answer.objects.values_list('qid', flat=True).get(id=id)
            instance = Answer.objects.filter(id=id).delete()
            return redirect(getans, id=qid)
        else:
            qid = Answer.objects.values_list('qid', flat=True).get(id=id)
            return redirect(getans, id=qid)


# edit profile for logged in user
@login_required
def editProfile(request):
    if request.method == "GET":
        usr = User.objects.get(username=request.user)
        userform = UserForm(instance=usr)
        prof = UserProfile.objects.get(user=request.user)
        proform = UserProfileForm(instance=prof)
        context = {
            'uform': userform,
            'pform': proform,
            'title': 'Edit profile'
        }
        return render(request, 'editProfile.html', context)
    else:
        uname = request.POST.get('username')
        email = request.POST.get('email')
        if User.objects.filter(username=uname).exists() and uname != request.user.username:
            usr = User.objects.get(username=request.user)
            userform = UserForm(instance=usr)
            prof = UserProfile.objects.get(user=request.user)
            proform = UserProfileForm(instance=prof)
            context = {
                'uform': userform,
                'pform': proform,
                'title': 'Edit profile',
                'umessage': "Username " + '"' + uname + '"' + " already exists"
            }
            return render(request, 'editProfile.html', context)
        elif User.objects.filter(email=email).exists() and email != request.user.email:
            usr = User.objects.get(username=request.user)
            userform = UserForm(instance=usr)
            prof = UserProfile.objects.get(user=request.user)
            proform = UserProfileForm(instance=prof)
            context = {
                'uform': userform,
                'pform': proform,
                'title': 'Edit profile',
                'emessage': '"' + email + '"' + " already exixts"
            }
            return render(request, 'editProfile.html', context)
        else:
            instance = User.objects.get(username=request.user)
            form = UserForm(request.POST or None, instance=instance)
            form.save()
            pic = request.FILES.get('pic')
            print(pic)
            if pic is None:
                return redirect(profile)
            else:
                prof = UserProfile.objects.get(user=request.user)
                prof.avatar = pic
                prof.save()
                return redirect(profile)


# deactivate account not Delete
def deleteProfile(request):
    user = request.user
    user.delete()
    return render(main)

# --------------------------------------------------------------------------------------------------------------ADMIN-----------------------------


@login_required(login_url='/login/')  # change here
def aadmin(request):
    if request.user.is_staff:  # here
        allusers = User.objects.all().order_by('username')
        avatar = UserProfile.objects.all()
        context = {
            'usrs': allusers,
            'profile': 'profile',
            'avatar': avatar,
        }
        return render(request, 'adminUserProfile.html', context)
    else:  # and here
        return HttpResponse('You dont have sufficient privilage to view this page')


def sendMail(request):
    mail = request.POST.get('mail')
    sub = request.POST.get('subject')
    bod = request.POST.get('body')
    print(mail)
    send_mail(sub, bod, settings.EMAIL_HOST_USER, [mail], fail_silently = False)
    return HttpResponse('')


@login_required(login_url='/login/')  # change here
def adminUserPosts(request):
    if request.user.is_staff:  # here
        qns = Question.objects.all().order_by('datetime').reverse()
        ans = Answer.objects.all().order_by('datetime').reverse()
        context = {
            'qns': qns,
            'ans': ans,
            'posts': 'posts'
        }
        return render(request, 'adminUserPosts.html', context)
    else:  # and here
        return HttpResponse('You dont have sufficient privilage to view this page')


@login_required(login_url='/login/')  # change here
def adminTags(request):
    if request.user.is_staff:  # here
        tags = Tag.objects.all().order_by('tag')
        context = {
            'tags': tags,
        }
        return render(request, 'adminTags.html', context)
    else:  # and here
        return HttpResponse('You dont have sufficient privilage to view this page')


@login_required(login_url='/login/')  # change here
def adminFeedback(request):
    if request.user.is_staff:  # here
        feed = Feedback.objects.all().order_by('email')
        context = {
            'feed': feed,
        }
        return render(request, 'adminFeedback.html', context)
    else:  # and here
        return HttpResponse('You dont have sufficient privilage to view this page')


@login_required(login_url='/login/')  # change here
def adminRemedies(request):
    if request.user.is_staff:  # here
        rem = Remedies.objects.all().order_by('disease')
        context = {
            'rem': rem,
        }
        return render(request, 'adminRemedies.html', context)
    else:  # and here
        return HttpResponse('You dont have sufficient privilage to view this page')


@login_required(login_url='/login/')  # change here
def adminImages(request):
    if request.user.is_staff:  # here
        hist = HistImage.objects.all().order_by('id').reverse()
        context = {
            'hist': hist,
        }
        return render(request, 'adminImages.html', context)
    else:  # and here
        return HttpResponse('You dont have sufficient privilage to view this page')


def addtag(request):
    if request.method == "POST":
        tag = request.POST.get('tag')
        tags = Tag(tag=tag)
        tags.save()
        return redirect(adminTags)
    else:
        return redirect(adminTags)


def editTag(request, id):
    if request.method == "GET":
        tag = Tag.objects.get(id=id)
        tagForm = TagForm(instance=tag)
        context = {
            'form': tagForm,
            'id': id
        }
        return render(request, 'editTag.html', context)
    else:
        instance = Tag.objects.get(id=id)
        form = TagForm(request.POST or None, instance=instance)
        form.save()
        return redirect(adminTags)


def admindeleteqn(request, id):
    if request.method == "GET":
        return render(request, 'adminconfirmDelete.html', {'id': id})
    else:
        if request.POST.get('yes') == 'yes':
            instance = Question.objects.filter(id=id).delete()
        return redirect(adminUserPosts)


def admindeleteans(request, id):
    if request.method == "GET":
        return render(request, 'adminconfirmDelAns.html', {'id': id})
    else:
        if request.POST.get('yes') == 'yes':
            instance = Answer.objects.filter(id=id).delete()
        return redirect(adminUserPosts)


def Ablock(request, id):
    u = User.objects.get(id=id)
    print(u)
    u.is_active = False
    u.save()
    print('block')
    return redirect(aadmin)


def Aunblock(request, id):
    u = User.objects.get(id=id)
    u.is_active = True
    u.save()
    return redirect(aadmin)


def changeRole(request, id):
    u = User.objects.get(id=id)
    if u.is_staff == True:
        u.is_staff = False
    else:
        u.is_staff = True
    u.save()
    return redirect(aadmin)


def changeExpert(request, id):
    u = UserProfile.objects.get(id=id)
    if u.is_expert == True:
        u.is_expert = False
    else:
        u.is_expert = True
    u.save()
    return redirect(aadmin)


def Adel(request, id):
    if request.method == "GET":
        print(id)
        return render(request, 'adminConfirmDeleteUser.html', {'id': id})
    else:
        if request.POST.get('yes') == 'yes':
            u = User.objects.get(username=id).delete()
        return redirect(aadmin)


def deltag(request, id):
    if request.method == "GET":
        return render(request, 'adminConfirmDeleteTag.html', {'id': id})
    else:
        if request.POST.get('yes') == 'yes':
            Tag.objects.get(id=id).delete()
        return redirect(adminTags)


def addRemedy(request):
    if request.method == "GET":
        form = remedyForm()
        context = {
            'form': form
        }
        return render(request, 'addRemedy.html', context)
    else:
        form = remedyForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(aadmin)
        else:
            return redirect(addRemedy)


def editRemedy(request, id):
    if request.method == "GET":
        rem = Remedies.objects.get(id=id)
        remForm = remedyForm(instance=rem)
        context = {
            'form': remForm,
            'id': id
        }
        return render(request, 'editRemedy.html', context)
    else:
        instance = Remedies.objects.get(id=id)
        form = remedyForm(request.POST or None, instance=instance)
        form.save()
        return redirect(aadmin)


def delRemedy(request, id):
    if request.method == "GET":
        return render(request, 'adminConfirmDeleteRemedy.html', {'id': id})
    else:
        if request.POST.get('yes') == 'yes':
            Remedies.objects.get(id=id).delete()
        return redirect(adminRemedies)


def delhist(request, id):
    if request.method == "GET":
        return render(request, 'adminConfirmDeleteImages.html', {'id': id})
    else:
        if request.POST.get('yes') == 'yes':
            HistImage.objects.get(id=id).delete()
        return redirect(adminImages)


def delFeed(request, id):
    if request.method == "GET":
        return render(request, 'adminConfirmDeleteFeedback.html', {'id': id})
    else:
        if request.POST.get('yes') == 'yes':
            Feedback.objects.get(id=id).delete()
        return redirect(adminFeedback)
