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

# 表示スケール
SCALE_D = 'd'
SCALE_M = 'm'
SCALE_Y = 'y'
# セルサイズ
CELL_SIZE_DEF = 21
CELL_SIZE_MIN = 20
CELL_SIZE_MAX = 100

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
    url = "gantt/"
    url = reverse_lazy('projects:gantt')

    def get(self, request, **kwargs):
        # scale,sizeをデフォルト値に設定
        self.request.session['scale'] = SCALE_M
        self.request.session['size'] = CELL_SIZE_DEF
        return super().get(request, **kwargs)

class gantt(generic.TemplateView):
    template_name = 'projects/gantt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        logger.info(str(self.request.user) + ' : ' + str(self.request.user.is_authenticated))

        # ガントチャートデータを生成、受け渡し
        context["gantt_data"] = createGanttData()

        return context

class scaleD(generic.RedirectView):
    url = reverse_lazy('projects:gantt')

    def get(self, request, **kwargs):
        # scaleのみ変更
        self.request.session['scale'] = SCALE_D
        return super().get(request, **kwargs)

class scaleM(generic.RedirectView):
    url = reverse_lazy('projects:gantt')

    def get(self, request, **kwargs):
        # scaleのみ変更
        self.request.session['scale'] = SCALE_M
        return super().get(request, **kwargs)

class sizeup(generic.RedirectView):
    url = reverse_lazy('projects:gantt')

    def get(self, request, **kwargs):
        # size変更
        size = self.request.session['size']
        if (size <= CELL_SIZE_MAX):
            size += CELL_SIZE_MIN
        self.request.session['size'] = size
        return super().get(request, **kwargs)

class sizedown(generic.RedirectView):
    url = reverse_lazy('projects:gantt')

    def get(self, request, **kwargs):
        # size変更
        size = self.request.session['size']
        if (size > (CELL_SIZE_MIN*2)):
            size -= CELL_SIZE_MIN
        self.request.session['size'] = size
        return super().get(request, **kwargs)

class add_prj(generic.CreateView):
    model = mdl_Project
    form_class = form_prj
    template_name = "projects/add_contents.html"
    success_url = reverse_lazy('projects:gantt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        # タイトル
        context["header_text"] = "プロジェクト追加"
        # レイアウト設定
        context["layout"] = "col-md-6 offset-md-3"
        return context

class add_tsk(generic.CreateView):
    model = mdl_Task
    form_class = form_tsk
    template_name = "projects/add_contents.html"
    success_url = reverse_lazy('projects:gantt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        # タイトル
        context["header_text"] = "タスク追加"
        # レイアウト設定
        context["layout"] = "col-md-6 offset-md-3"
        return context
