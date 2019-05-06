from django.urls import path
from . import views

urlpatterns = [
    path('', views.top.as_view(), name='top'),
    path('<str:scale>/', views.gantt.as_view(), name='gantt'),
    path('add_prj/', views.add_prj.as_view(), name='add_prj'),
    path('add_tsk/', views.add_tsk.as_view(), name='add_tsk'),
]