from django.shortcuts import render
from django.views import generic
from .models import mdl_Project, mdl_Task

# ログ設定
import logging
logger = logging.getLogger('command')

class top(generic.ListView):
    model = mdl_Project
    template_name = 'projects/gantt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す

        logger.info(str(self.request.user) + ' : ' + str(self.request.user.is_authenticated))
        
        context.update({
            'mdl_prj' : mdl_Project.objects.all(),
            'mdl_tsk' : mdl_Task.objects.all(),
        })

        return context
