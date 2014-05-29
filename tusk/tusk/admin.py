from django.contrib import admin
from tusk.models import  Project, Iteration, Entry, Task, Story, Dev
from tusk.forms import addDevForm




class DevAdmin(admin.ModelAdmin):
    form = addDevForm



admin.site.register(Project)
admin.site.register(Iteration)
admin.site.register(Entry)
admin.site.register(Task)
admin.site.register(Dev, DevAdmin)
admin.site.register(Story)
