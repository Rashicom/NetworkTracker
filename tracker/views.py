from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class Home(View):

    def get(self,request):
        """
        fetch the system information and render the index page
        """
        return HttpResponse("")


class SystemInfo(View):
    form_class = ""

    def post(self,request):
        """
        """
        pass
        
