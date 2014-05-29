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










"""
class Developer(models.Model):
	name = models.CharField(max_length=25, blank = False)
	# a new registered user can have his own team of developers for projects:
	user = models.ForeignKey(User)
	project = models.ManyToManyField(Project)
	date = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.name

	def clean(self):
		from django.core.exceptions import ValidationError
		if self.name == '':
			raise ValidationError('Enter Devs name')
"""


class Dev(User):
	"""
	Developer users
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
	dev = models.ManyToManyField(Dev, related_name='Dev')
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
	description = models.TextField(max_length=1000)
	start_time = models.DateTimeField(blank = True, null=True)
	end_time = models.DateTimeField(blank = True, null=True)
	time_paused = models.PositiveIntegerField(default=0)
	task = models.ForeignKey(Task)



	class Meta:
		verbose_name_plural="Entries"

	def __unicode__(self):
		return self.description

	def get_total_time(self):
		"""
        Gets total time spent for each Task's Entry in seconds. Takes paused seconds into account.
        If there's no end_time (the Entry is paused), end time is request time.
        """
		if not end_time:
			end_time = self.pause_time if self.is_paused else timezone.now()
			total_time = self.end_time - self.start_time
			seconds = total_time.seconds - self.get_paused_seconds()
			return seconds + (total_time.days * 86400)

	def is_paused(self):
		"""
		Check if Entry is paused
		"""
		return bool(self.pause_time)

	def pause(self):
		"""
		pause Entry
		"""
		if not self.time_paused:
			self.time_paused = timezone.now()

	def unpause(self, date=None):
		"""
        Unpause Entry
        """
		if self.is_paused:
			if not date:
				date = timezone.now()
				delta = date - self.pause_time
				self.seconds_paused += delta.seconds
				self.pause_time = None

	def get_paused_seconds(self):
		pass





