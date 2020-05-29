from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class MyinfoView(TemplateView):
    template_name = 'myinfo.html'