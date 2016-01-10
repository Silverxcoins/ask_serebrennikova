from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib import auth
from ask.models import Question, Answer, Tag, Profile, Like
from ask.paginate import paginate
from django.core.paginator import Paginator
from ask.forms import UserForm, SettingsForm, QuestionForm, AnswerForm

def getAuthenticatedUser(request):
	if request.user.is_authenticated():
		user = Profile.objects.get(user_ptr_id=request.user.id)
	else:
		user = None
	return user

def index(request, page=None):
    questions = Question.objects.newest()
    questions_on_page = paginate(questions, request, 10, page)
    return render(request, 'ask/index.html', {
	'questions':  questions_on_page,
	'page': page,
    })

def hot(request, page=None):
    questions = Question.objects.hot()
    questions_on_page = paginate(questions, request, 10, page)
    return render(request, 'ask/hot.html', {
	'questions':  questions_on_page,
	'page': page,
    })

def tag(request, tag_name, page=None):
    questions = Question.objects.tag(tag_name=tag_name)
    questions_on_page = paginate(questions, request, 10, page)
    return render(request, 'ask/tag.html', {
	'questions':  questions_on_page,
	'page': page,
	'tag': tag_name,
    })

def question(request, question_id, page=None):
    ques = Question.objects.get(id=question_id)
    answers = ques.answer_set.all()
    answers_on_page = paginate(answers, request, 10, page)
    User = getAuthenticatedUser(request)
    if User != None:
        if request.POST:
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.saveAnswer(User, question_id)
                page = answers.count() / 10
                if (answers.count() % 10 != 0):
                    page += 1
                return redirect('/question/' + str(question_id) + '/' + str(page))
        else:
            form = AnswerForm()
    else:
        form = AnswerForm()
    return render(request, 'ask/question.html', {
	'answers': answers_on_page,
	'question': ques, 
	'page': page,
        'form' : form,
    })
    

def signup(request):
    if request.POST:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid_():
            user = form.saveUser()
            return redirect('/')
        else:
            return render(request, 'ask/signup.html', { 'form' : form })
    else:
        form = UserForm()
        return render(request, 'ask/signup.html', { 'form' : form })

def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            redirect_to = request.GET.get('next')
            auth.login(request,user)
            return redirect(redirect_to)
        else:
            return render(request, 'ask/login.html', { 'error' : 'wrong login-password combination'})
    else:
        return render(request, 'ask/login.html')

def logout(request):
    auth.logout(request)
    redirect_to = request.GET.get('next')
    return redirect(redirect_to)

def ask(request):
    if request.user.is_authenticated():
        User = getAuthenticatedUser(request)
        if request.POST:
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.saveQuestion(User)
                return redirect('/question/' + str(question.id))
        else:
            form = QuestionForm()
        return render(request, 'ask/ask.html', { 'form' : form })
    else:
        return redirect('/')


def settings(request):
    if request.user.is_authenticated():
        User = getAuthenticatedUser(request)
        if request.POST:
            form = SettingsForm(request.POST)
            if form.is_valid_():
                user = form.saveSettings(User)
        else:
            form = SettingsForm()
        return render(request, 'ask/settings.html', { 'form' : form, 'nickname' : User.nickname })
    else:
        return redirect('/')

def like(request):
    if request.method == 'POST':
        response_data = {}

        user = getAuthenticatedUser(request)

        object_id = int(request.POST.get('object_id',''))
        like_type = int(request.POST.get('like_type',''))
        object_type = request.POST.get('object_type','')

        if user:
            new_rating = None
            error = None

            if object_type == 'answer':
                answ = Answer.objects.get(id=object_id)

                if (answ.correct == True):
                    answ.correct = False
                else:
                    answ.correct = True
                answ.save()

            elif object_type == 'question':
                quest = Question.objects.get(id=object_id)

                if user != quest.user:
                    try:
                        like = Like.objects.filter(question_id=object_id).get(author_id=user.id)
                        error = 'You can vote only once!'
                    except:
                        like = Like.objects.create(author=user, like_type=like_type, question=quest)
                        like.save()
                        quest.rating += like_type
                        quest.save()
                        new_rating = quest.rating
                else:
                    error = 'It is your question!'
            else:
                error = 'Object not found!'

            if new_rating:
                response_data['new_rating'] = new_rating
            if error:
                response_data['error'] = error
        else:
            response_data['error'] = 'User is not authenticated!'

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "No POST data!"})




