from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import NetworkSystems, SystemProcesses, ProcessHistory


class Home(View):

    def get(self,request):
        """
        fetch the system information and render the index page
        """

        users = NetworkSystems.objects.all()
        return render(request, "home.html", {"users": users})


class ProcessesInfo(View):

    def get(self, request,user_id):
        """
        fetch all the process of the user
        """
        process_list = SystemProcesses.objects.filter(network_system=user_id)
        return render(request, "process.html", {"process_list": process_list})



class UsageHistory(View):

    def get(self,request,process_id):
        """
        returns the process hisstory of a perticular process
        """
        process_history = ProcessHistory.objects.filter(system_package=process_id)
        print(process_history)
        return render(request, "history.html",{'process_history':process_history})
        
