from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from ask.models import Profile, Question, Answer, Tag, Like
from loremipsum import get_sentence, get_paragraph, get_sentences, get_paragraphs
from random import randint, randrange
from datetime import timedelta, datetime

users_count = 10001
questions_count = 100001
answers_count = 1000001
tags_count = 10001
likes_count = 2000001


class Command(BaseCommand):
	def handle(self, *args, **options):

		start_time = datetime.now()

		"""admin = Profile(	
					id = 1,
					avatar='http://lorempixel.com/81/81',
					password=make_password("blabla"), 
					last_login=self.random_date(),
					is_superuser=True, 
					username="serebrennik", 
					first_name="", 
					last_name="", 
					email="sasha.serebrennik@gmail.com", 
					is_staff=True, 
					is_active=True,
					date_joined=self.random_date())
		admin.save()

		for user_id in range(2, users_count + 1):
			if user_id % 10 == 0:
				self.stdout.write("user: " + str(user_id))

			user = Profile(	
					avatar='http://lorempixel.com/8%s/8%s' % (user_id % 10, user_id % 10), 
					id=user_id, 
					password=make_password("secret"), 
					last_login=self.random_date(),
					is_superuser=False, 
					username="user%s" % (user_id), 
					first_name="", 
					last_name="", 
					email="", 
					is_staff=False, 
					is_active=True,
					date_joined=self.random_date())
			user.save()

		for question_id in range(1, questions_count + 1):
			if question_id % 10 == 0:
				self.stdout.write("question: " + str(question_id))
			
			text = ''
                        for i in get_paragraphs(randint(1,3)):
                                text += i

			question = Question(
					id=question_id, 
					title=get_sentence(),	
					text=text, 
					user_id=randint(1, users_count),		#CustomUser.objects.get(pk=randint(1, users_count)), 
					created=self.random_date(),
					rating=0)
			question.save()

		
		for answer_id in range(843888, answers_count + 1):
			if answer_id % 100 == 0:
				self.stdout.write("answer: " + str(answer_id))
			
			text = ''
                        for i in get_paragraphs(randint(1,2)):
                            text += i
                        
                        if (randint(0,1) == 0):
                            correct = False
                        else:
                            correct = True

			answer = Answer(
					id=answer_id, 
					text=text, 
					user_id=randint(1, users_count),		
					created=self.random_date(),
					question_id=randint(1, questions_count),
                                        correct=correct)
			answer.save()

		words = open('ask/words', 'r')
		tag_id = 1
		for tag_id in range(1, tags_count + 1):
			self.stdout.write("tag: " + str(tag_id))
			tag = Tag(
					id=tag_id, 
					name=words.readline()[:-1])
			tag.save()
		words.close()

		for question_id in range(1, questions_count + 1):
			if question_id % 10 == 0:
				self.stdout.write('Linking tags with question:' + str(question_id))

			question = Question.objects.get(pk=question_id)
			for i in range(1, 4):
				question.tags.add(Tag.objects.get(pk=randint(1, tags_count)))


		for like_id in range(1, likes_count + 1):
			
			value = -1 if randint(0, 1) == 0 else 1
			like = Like(
					id=like_id,
					like_type=value,
					question_id=randint(1, questions_count),
					author_id=randint(1, users_count))
			try:
				like.save()
				if like_id % 10 == 0:
					self.stdout.write('like:' + str(like_id))
			except IntegrityError:
				pass"""


		for question in Question.objects.all():
			for like in question.like_set.all():
				question.rating += like.like_type
				if like.id % 10 == 0:
					self.stdout.write('question: ' + str(question.id) + ', like: ' + str(like.id))
			question.save()


		end_time = datetime.now()
		
		self.stdout.write('Database filled successfully' + str(end_time - start_time))

	def random_date(self):

		start = datetime(2014, 1, 1, 1, 0, 0, 0, None)
		end = datetime(2015, 1, 1, 1, 0, 0, 0, None)

		delta = end - start
		int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
		random_second = randrange(int_delta)
		return start + timedelta(seconds=random_second)
