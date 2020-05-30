from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class LikeFeedView(TemplateView):
    template_name = 'likefeed.html'