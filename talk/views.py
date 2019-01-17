from django.shortcuts import render,get_object_or_404
from .models import Talk
import markdown
def talking(request):
    talk_list=Talk.objects.all().order_by('-created_time')

    return render(request,'myblog/talking.html',context={'talk_list':talk_list})

def archives1(request,year,month):
    talk_list=Talk.objects.filter(created_time__year=year,
                                  created_time__month=month
                                  ).order_by('-created_time')
    return render(request,'myblog/talking.html',context={'talk_list':talk_list})


# Create your views here.
