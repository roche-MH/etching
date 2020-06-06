from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class tonemeupView(TemplateView):
    template_name = 'tonemeup.html'