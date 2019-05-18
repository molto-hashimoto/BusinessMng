from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy, reverse

from users.models import User
from .models import mdl_Project, mdl_Task
from .forms import form_prj, form_tsk

import json

# ログ設定
import logging
logger = logging.getLogger('command')

def createGanttData():
    
    prj_data = []
    prjs = mdl_Project.objects.all()

    for idx,prj in enumerate(prjs):

        series = []
        tsks = prj.mdl_task_set.all()

        for idx2,tsk in enumerate(tsks):
            t = {}
            t['name'] = tsk.name
            t['start'] = tsk.start.isoformat()
            t['end'] = tsk.end.isoformat()
            series.append(t)

        dict = {}
        dict['id'] = idx
        dict['name'] = prj.name
        dict['series'] = series

        prj_data.append(dict)

    return prj_data

# ガントチャートデフォルトスケール月単位でリダイレクトする
class top(generic.RedirectView):
    url = "gantt/m/21"

class gantt(generic.TemplateView):
    template_name = 'projects/gantt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        logger.info(str(self.request.user) + ' : ' + str(self.request.user.is_authenticated))

        context["gantt_data"] = createGanttData()
        context["scale"] = self.kwargs.get('scale')
        context["size"] = self.kwargs.get('size')
        return context

class sizeup(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        size = self.kwargs['size']
        if (size <= 100):
            size += 20
        self.url = reverse('projects:gantt', kwargs={'scale': self.kwargs['scale'], 'size': size})
        return super().get_redirect_url(*args, **kwargs) 

class sizedown(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        size = self.kwargs['size']
        if (size > 40):
            size -= 20
        self.url = reverse('projects:gantt', kwargs={'scale': self.kwargs['scale'], 'size': size})
        return super().get_redirect_url(*args, **kwargs) 

class add_prj(generic.CreateView):
    model = mdl_Project
    form_class = form_prj
    template_name = "projects/add_contents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        # タイトル
        context["header_text"] = "プロジェクト追加"
        # レイアウト設定
        context["layout"] = "col-md-6 offset-md-3"
        context["scale"] = self.kwargs.get('scale')
        context["size"] = self.kwargs.get('size')
        return context

    def get_success_url(self):
        self.success_url = reverse('projects:gantt', kwargs={'scale': self.kwargs['scale'], 'size': self.kwargs['size']})
        return self.success_url

class add_tsk(generic.CreateView):
    model = mdl_Task
    form_class = form_tsk
    template_name = "projects/add_contents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        # タイトル
        context["header_text"] = "タスク追加"
        # レイアウト設定
        context["layout"] = "col-md-6 offset-md-3"
        context["scale"] = self.kwargs.get('scale')
        context["size"] = self.kwargs.get('size')
        return context

    def get_success_url(self):
        self.success_url = reverse('projects:gantt', kwargs={'scale': self.kwargs['scale'], 'size': self.kwargs['size']})
        return self.success_url