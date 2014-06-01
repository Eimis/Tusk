from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from tusk.models import Project, Iteration, Entry, Task, Story, Dev
from tusk.forms import IterationForm, TaskForm, addDevForm
from django.contrib.sites.models import Site
import datetime
from django.utils import timezone, simplejson
from django.core import serializers


from django.shortcuts import render

def Main(request):
    '''
    Landing page
    '''
    if request.method == 'POST':
    	form = AuthenticationForm(data = request.POST)
    	errors = form.errors
    	if form.is_valid():
    		username = request.POST['username']
    		password = request.POST['password']
    		user = authenticate(username=username, password=password)
    		login(request, user)
    		return HttpResponseRedirect('/dashboard/')
    	else:
    		return render(request, "main.html", {"form": form, "errors" : errors})
    form = AuthenticationForm()
    return render(request, "main.html", {"form" : form,})


def Register(request):
    '''
    Adds a new user (Project manager) to the system. This is not a Developer.
    '''
    if request.method == 'POST':
    	form = UserCreationForm(request.POST)
    	errors = form.errors
        if form.is_valid():
    		user = form.save()
    		username = request.POST['username']
    		password = request.POST['password1']
    		user = authenticate(username=username, password=password)
    		login(request, user)
    		return HttpResponseRedirect('/dashboard/')
    	else:
    		return render(request, "register.html", {"form": form, "errors" : errors})
    form = UserCreationForm()

    return render(request, "register.html", {"form" : form})



@login_required(redirect_field_name=None)
def Logout(request):
	logout(request)
	return HttpResponseRedirect("/")


@login_required(redirect_field_name=None)
def Dashboard(request):
    """
    Dashboard displays a list of user Projects or a list of Projects that
    Dev is assigned to.
    """
    user = request.user
    projects = user.project_set.all().order_by('-date')
    domain = Site.objects.get_current().domain
    return render(request, "dashboard.html", {"user" : user, "projects" : projects, "domain" : domain})


@login_required(redirect_field_name=None)
def New_project(request):
    if request.method == 'POST':
    	user = request.user
    	new_project = Project(project_title = request.POST['project_title'], project_description = request.POST['project_description'], user = user)
    	new_project.save()
        #creating a new Iteration because each project has to have "Iteration zero":
        new_iteration = Iteration(user = user, project = new_project, name = "Iteration zero")
        new_iteration.save()
    	return HttpResponseRedirect("/dashboard/")
    else:
        return HttpResponseRedirect("/dashboard/")

@login_required(redirect_field_name=None)
def Project_view(request, slug):
    """
    A Project view with User stories, tasks, iterations, their time, etc.
    """
    domain = Site.objects.get_current().domain
    user = request.user
    project = Project.objects.get(user=user, slug=slug)
    title = project.project_title
    description = project.project_description
    iterations = Iteration.objects.filter(user = user, project = project).order_by('-date')
    stories = Story.objects.filter(user = user, project = project).order_by('-date')
    form = IterationForm
    taskForm = TaskForm(request.POST, project = project)
    addDev = addDevForm(request.POST)
    if request.method == 'POST':
        form = IterationForm
        if form.is_valid():
            user = request.user
            project = Project.objects.get(user=user, slug=slug)
            new_iteration = Iteration(user = request.user, duration = form.cleaned_data['duration'], project = Project.objects.get(user=user, slug=slug), name = form.cleaned_data['name'],)
            new_iteration.save()
            return HttpResponseRedirect("/dashboard/")



    try:
        developers = Dev.objects.filter(user = request.user, project = project)
        return render(request, "project.html", {"title" : title, "description" : description, "iterations" : iterations, "developers" : developers, "domain" : domain, "form" : form, "stories" : stories, "taskForm" : taskForm, "addDev" : addDev})
    except Developer.DoesNotExist:
        return render(request, "project.html", {"title" : title, "description" : description, "iterations" : iterations, "domain" : domain, "form" : form, "stories" : stories, "taskForm" : taskForm, "addDev" : add})
    

@login_required(redirect_field_name=None)
def New_iteration(request, slug):
    form = IterationForm()
    user = request.user
    project = Project.objects.get(user=user, slug=slug)
    domain = Site.objects.get_current().domain
    if request.method == 'POST':
        form = IterationForm(request.POST)
        errors = form.errors
        if form.is_valid():
            user = request.user
            project = Project.objects.get(user=user, slug=slug)
            new_iteration = Iteration(user = request.user, duration = form.cleaned_data['duration'], project = Project.objects.get(user=user, slug=slug), name = form.cleaned_data['name'])
            new_iteration.save()
            return HttpResponseRedirect(domain + slug)
        else:
            return render(request, "new_iteration.html", {"errors" : errors, "form" : form})
    return render(request, "new_iteration.html", {"form" : form, "project" : project, "user" : user})


@login_required(redirect_field_name=None)
def New_developer(request, slug):
    """
    Creates (and assigns) a new Developer to current project that Project manager is in.
    """
    if request.method == 'POST':
        user = request.user
        project = Project.objects.get(user=user, slug=slug)
        form = addDevForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/" + project.slug)
        else:
            return HttpResponse("form not valid")
    else:
        return HttpResponseRedirect("/dashboard/")

@login_required
def New_story(request, slug):
    user = request.user
    project = Project.objects.get(user=user, slug=slug)
    domain = Site.objects.get_current().domain
    if request.method == 'POST':
        new_story = Story(user = user, project = project, title = request.POST['title'])
        new_story.save()
        return HttpResponseRedirect(domain + slug)
    else:
        return HttpResponse('Req. not POST')

@login_required
def New_task(request, slug):
    """
    Creates a new Task with selected Developers for this Task.
    """
    user = request.user
    project = Project.objects.get(user = user, slug = slug)
    domain = Site.objects.get_current().domain
    if request.method == 'POST':
        user = request.user
        form = TaskForm(request.POST, project = project)
        if form.is_valid():
            new_task = Task(user = user, project = project, iteration = form.cleaned_data['iteration'], story = form.cleaned_data['story'], description = form.cleaned_data['description'])
            new_task.save()
            for dev in form.cleaned_data['dev']:
                new_task.dev.add(dev.pk) # because of m2m field
            return HttpResponseRedirect(domain + slug)


@login_required
def Task_view(request,slug, id):
    """
    A view for displaying Task with its info, time, new time Entries
    for task will be added from this view.
    """
    user = request.user
    project = Project.objects.get(user = user, slug = slug)
    task = Task.objects.get(pk = id)
    developers = Dev.objects.filter(Task__id = task.pk)
    domain = Site.objects.get_current().domain
    return render(request, "task.html", {"task" : task, "developers" : developers, "domain" : domain})


def New_entry(request):
    user = request.user
    project = Project.objects.get(user=user, slug=slug)
    new_entry = Entry(project = project)


def Start_entry(request, slug, id):
    """
    Time spent for Entry starts counting when a request to this view is fired.
    """
    entry = Entry.objects.get(pk = id)
    entry.start_time = timezone.now()
    entry.save()
    return HttpResponseRedirect("/dashboard/")

def End_entry(request, slug, id):
    entry = Entry.objects.get(pk = id)
    entry.end_time = timezone.now()
    entry.save()
    return HttpResponseRedirect("/dashboard/")

def Get_total_time(request, slug, id):
    """
    Using Ajax, gets total time spent for each Task's Entry in seconds. Takes paused seconds into account.
    If there's no end_time (the Entry is paused), end time is request's time.
    """
    entry = Entry.objects.get(pk = id)
    if not entry.end_time:
        entry.end_time = entry.time_paused if entry.is_paused else timezone.now()
    entry.total_time = entry.end_time - entry.start_time
    seconds = entry.total_time.seconds
    a = seconds + (entry.total_time.days * 86400)
    return HttpResponse(a)


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


def Get_tasks(request, slug):
    """
    Gets a list of Tasks for selected Iteration. Also gets Task's pk for generating links in a dropdown dynamically using Ajax in Project_view.
    """
    user = request.user
    project = Project.objects.get(user = user, slug = slug)
    if request.method == 'POST' and request.is_ajax():
        iteration = Iteration.objects.get(user = user, project = project, name = request.POST['Iterations'])
        tasks_query = Task.objects.filter(user = user, iteration = iteration)
        task_list = []
        for x in tasks_query:
            task_list.append(x.description)
        pk_list = []
        for y in tasks_query:
            pk_list.append(y.pk)
        tasks = zip(task_list, pk_list)
        response = HttpResponse(simplejson.dumps(tasks),mimetype='application/json')
        return response
    else:
        return HttpResponse("Request not post or ajax")

