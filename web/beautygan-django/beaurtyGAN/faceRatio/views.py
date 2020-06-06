from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class faceRatioView(TemplateView):
    template_name = 'faceRatio.html'