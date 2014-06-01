from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime
from django.utils import timezone

class Project(models.Model):
    user = models.ForeignKey(User)
    project_title = models.TextField(max_length=1000)
    project_description = models.TextField(max_length=1000)
    slug = models.SlugField(blank = True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.project_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.project_title)
        super(Project, self).save(*args, **kwargs)


class Iteration(models.Model):
	user = models.ForeignKey(User)
	one_two = '1-2 weeks'
	two_four = '2-4 weeks'
	four_six = '4-6 weeks'
	six_eight = '6-8 weeks'
	DURATION_CHOICES = (
        (one_two, '1-2 weeks'),
        (two_four, '2-4 weeks'),
        (four_six, '4-6 weeks'),
        (six_eight, '6-8 weeks'),
    )
	name = models.TextField(max_length=1000)
	duration = models.CharField(max_length=100, choices=DURATION_CHOICES, default=two_four, blank = True)
	project = models.ForeignKey(Project)
	date = models.DateTimeField(auto_now_add=True)
	def is_upperclass(self):
		return self.duration in (self.one_two, self.six_eight)

	def __unicode__(self):
		return self.name



class Story(models.Model):
	user = models.ForeignKey(User)
	title = models.TextField(max_length=1000)
	project = models.ForeignKey(Project)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name_plural="Stories"


class Dev(User):
	"""
	A model to describe a Developer. This is actually just a simple User class.
	He will be able to login to the system and see Projects that he is assigned to.
	Only Users (Project managers) that are registered via the main Registration form will be able to add new Developers.
	new Devs - 
	TODO: remove permissions to create Projects / add new Developers.
	"""
	user = models.ForeignKey(User, related_name='user')
	project = models.ForeignKey(Project)

	class Meta:
		verbose_name="Dev"
		verbose_name_plural="Devs"

	def __unicode__(self):
		return self.username


class Task(models.Model):
	user = models.ForeignKey(User)
	iteration = models.ForeignKey(Iteration)
	story = models.ForeignKey(Story)
	description = models.TextField(max_length=1000)
	project = models.ForeignKey(Project)
	dev = models.ManyToManyField(Dev, related_name='Task')
	not_started = 'Not started'
	in_progress = 'In progress'
	done = 'Done'
	TASK_STATUS_CHOICES = (
        (not_started, 'Not started'),
        (in_progress, 'In progress'),
        (done, 'Done'),
    )
	status = models.CharField(max_length=100, choices=TASK_STATUS_CHOICES, blank = True)

	def __unicode__(self):
		return self.description

class Entry(models.Model):
	"""
	A model describing the smallest element of the App - time Entry
	for each Task.
	"""
	description = models.TextField(max_length=1000)
	start_time = models.DateTimeField(blank = True, null=True)
	end_time = models.DateTimeField(blank = True, null=True)
	time_paused = models.PositiveIntegerField(default=0)
	task = models.ForeignKey(Task)



	class Meta:
		verbose_name_plural="Entries"

	def __unicode__(self):
		return self.description