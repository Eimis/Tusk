from django.conf.urls import patterns, include, url
from tusk.views import Main, Register, Dashboard,  Logout, New_project, Project_view, New_iteration, New_developer, Task_view, Start_entry, End_entry, Get_total_time, Get_tasks, New_story, New_task

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', Main),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^register/$', Register),
	url(r'^logout/$', Logout),
	url(r'^dashboard/$', Dashboard),
	url(r'^new_project/$', New_project),
	url(r'^(?P<slug>[-\w]+)/task/(?P<id>[-\w]+)$', Task_view),
	url(r'^(?P<slug>[-\w]+)/task/start_entry/(?P<id>[-\w]+)/$', Start_entry),
	url(r'^(?P<slug>[-\w]+)/task/end_entry/(?P<id>[-\w]+)/$', End_entry),
	url(r'^(?P<slug>[-\w]+)/task/get_total_time/(?P<id>[-\w]+)/$', Get_total_time),
	url(r'^(?P<slug>[-\w]+)/new_developer/$', New_developer),
	url(r'^(?P<slug>[-\w]+)/new_iteration/$', New_iteration),
	url(r'^(?P<slug>[-\w]+)/new_story/$', New_story),
	url(r'^(?P<slug>[-\w]+)/new_task/$', New_task),
	url(r'^(?P<slug>[-\w]+)/get_tasks/$', Get_tasks),
    url(r'^(?P<slug>[-\w]+)/$', Project_view),
)
