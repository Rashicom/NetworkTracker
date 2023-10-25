from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home.as_view()),
    path('processes/<str:user_id>', views.ProcessesInfo.as_view(), name="processes"),
    path('process_history/<str:process_id>',views.UsageHistory.as_view(),name="process_history"),

]

