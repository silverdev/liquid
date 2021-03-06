from django.shortcuts import render_to_response
from intranet.models import Job
from django.template import RequestContext
from django.contrib import messages
from intranet.job_manager.forms import JobFormSet
from django.contrib.auth.decorators import user_passes_test
from utils.group_decorator import group_admin_required


@group_admin_required(['Corporate'])
def main(request):
   if request.method == 'POST':
      formset = JobFormSet(request.POST)
      if formset.is_valid(): # All validation rules pass
         formset.save()
         messages.add_message(request, messages.SUCCESS, 'Changes saved')
   jobs = Job.objects.filter(sent__exact=False).filter(status__exact='defer')
   formset = JobFormSet(queryset=jobs)
   return render_to_response('intranet/job_manager/main.html',{"section":"intranet","page":'jobs',"job_count":len(jobs),"jobs":formset},context_instance=RequestContext(request))