from django import forms
from ask.models import Profile, Question, Answer, Tag

class UserForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    email    = forms.EmailField(widget = forms.EmailInput(attrs = {'class' : 'form-control'}))
    nickname = forms.CharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'form-control'}))
    repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'form-control'}))
    avatar = forms.ImageField()

    def is_valid_(self):
        ret = self.is_valid()
        if len(Profile.objects.filter(username=self.cleaned_data.get('username'))) > 0:
            self.add_error('username', 'This username is already exist')
            ret = False
        if len(Profile.objects.filter(email=self.cleaned_data.get('email'))) > 0:
            self.add_error('email', 'This email is already exist')
            ret = False
        if self.cleaned_data.get('password') != self.cleaned_data.get('repeat_password'):
            self.add_error('password', '')
	    self.add_error('repeat_password', 'Passwords don`t match')
            ret = False
        return ret

    def saveUser(self):
        if self.is_valid_():
            user = Profile.objects.create_user(username=self.cleaned_data.get('username'),
                                                  email=self.cleaned_data.get('email'),
                                                  nickname=self.cleaned_data.get('nickname'),
                                                  password=self.cleaned_data.get('password'),
                                                 )
            user.avatar = self.cleaned_data.get('avatar')
            user.save()
            return True
        return False



class SettingsForm(forms.Form):
    email    = forms.EmailField(widget = forms.EmailInput(attrs = {'class' : 'form-control'}), required=False)
    nickname = forms.CharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}), required=False)
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'form-control'}), required=False)
    repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'form-control'}), required=False)
    avatar = forms.ImageField(required=False)

    def is_valid_(self):
        ret = self.is_valid()
        if len(self.cleaned_data.get('email')) > 0:
            if len(Profile.objects.filter(email=self.cleaned_data.get('email'))) > 0:
                self.add_error('email', 'This email is already exist')
                ret = False
        if len(self.cleaned_data.get('password')) > 0:
            if self.cleaned_data.get('password') != self.cleaned_data.get('repeat_password'):
                self.add_error('password', '')
	        self.add_error('repeat_password', 'Passwords don`t match')
                ret = False
        return ret

    def saveSettings(self,user):
        if self.is_valid_():
            if len(self.cleaned_data.get('email')) > 0:
                user.email = self.cleaned_data.get('email')
            if len(self.cleaned_data.get('nickname')) > 0:
                user.nickname = self.cleaned_data.get('nickname')
            if len(self.cleaned_data.get('password')) > 0:
                user.password = self.cleaned_data.get('password')
            user.avatar = self.cleaned_data.get('avatar')
            user.save()
            return True
        return False

class QuestionForm(forms.Form):
    title = forms.CharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}), required=False)
    text  = forms.CharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}), required=False)
    tags  = forms.CharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}), required=False)

    def saveQuestion(self, user):
        question = Question.objects.create(
                   user = user,
                   title = self.cleaned_data.get('title'),
                   text = self.cleaned_data.get('text'),
                   )
        tags = self.cleaned_data.get('tags').split(',')
        for tag in tags:
            if ' ' in tag:
                tag = tag.replace(' ', '_')
            if len(Tag.objects.filter(name=tag)) > 0:
                t = Tag.objects.get(name = tag)
            else:
                t = Tag.objects.create(name = tag)
                t.save()
            question.tags.add(t)
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}))

    def saveAnswer(self, user, question_id):
        answ = Answer.objects.create(
               user = user,
               text = self.cleaned_data.get('text'),
               question_id = question_id,
               correct = False,
               )
        answ.save()

        return answ


    
    
    
