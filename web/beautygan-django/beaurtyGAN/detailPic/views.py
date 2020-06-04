from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class DetailPicView(TemplateView):
    template_name = 'detailPic.html'