from django.forms import ModelForm
from tusk.models import Iteration, Task, Project, Dev
from django import forms
from django.contrib.auth.forms import UserCreationForm





class IterationForm(ModelForm):
	class Meta:
		model = Iteration
		fields = ('name', 'duration',)

	def __init__(self, *args, **kwargs):
		super(IterationForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget = forms.Textarea(attrs={'rows' : '1', 'class' : 'form-control'})
		self.fields['duration'].widget.attrs['class'] = 'form-control'

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ('iteration', 'story', 'description', 'dev')

	def __init__(self, *args, **kwargs):
		self.project = kwargs.pop('project')
		super(TaskForm, self).__init__(*args, **kwargs)
		self.fields['description'].widget = forms.Textarea(attrs={'rows' : '5', 'class' : 'form-control'})
		self.fields['iteration'].widget.attrs['class'] = 'form-control'
		self.fields['story'].widget.attrs['class'] = 'form-control'
		self.fields['dev'] = forms.ModelMultipleChoiceField(queryset = Dev.objects.filter(project = self.project))




class addDevForm(forms.ModelForm):
    class Meta:
        model = Dev
        fields = ('username','password', 'user', 'project')
        widgets = {'password': forms.PasswordInput(),}

    def save(self, commit=True):
        user = super(addDevForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



