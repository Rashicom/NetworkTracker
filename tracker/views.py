from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class test(View):

    def get(self,request):
        return HttpResponse("hello there")
