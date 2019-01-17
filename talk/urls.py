from django.conf.urls import url
from . import views

app_name='talk'
urlpatterns=[
    url(r'^talking/$',views.talking,name='talking'),
]