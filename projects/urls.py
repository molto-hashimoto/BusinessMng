from django.urls import path
from . import views

urlpatterns = [
    path('', views.top.as_view(), name='top'),
    path('add_prj/<str:scale>/<int:size>', views.add_prj.as_view(), name='add_prj'),
    path('add_tsk/<str:scale>/<int:size>', views.add_tsk.as_view(), name='add_tsk'),
    path('gantt/<str:scale>/<int:size>', views.gantt.as_view(), name='gantt'),
    path('sizeup/<str:scale>/<int:size>', views.sizeup.as_view(), name='sizeup'),
    path('sizedown/<str:scale>/<int:size>', views.sizedown.as_view(), name='sizedown'),
]