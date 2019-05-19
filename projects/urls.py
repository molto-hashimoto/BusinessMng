from django.urls import path
from . import views

urlpatterns = [
    path('', views.top.as_view(), name='top'),
    path('add_prj/', views.add_prj.as_view(), name='add_prj'),
    path('add_tsk/', views.add_tsk.as_view(), name='add_tsk'),
    path('gantt/', views.gantt.as_view(), name='gantt'),
    path('scaleD/', views.scaleD.as_view(), name='scaleD'),
    path('scaleM/', views.scaleM.as_view(), name='scaleM'),
    path('sizeup/', views.sizeup.as_view(), name='sizeup'),
    path('sizedown/', views.sizedown.as_view(), name='sizedown'),
]