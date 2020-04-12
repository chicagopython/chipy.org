from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.urls import reverse 
from chipy_org.apps.job_board.forms import JobPostForm, JobUserForm, JobProfileForm
from django.contrib.auth.decorators import login_required
from .models import JobPost
from django.db.models import Q

@login_required
def create_job_post(request):


    if request.method == 'POST':
      
        job_post_form = JobPostForm(request.POST)
        job_user_form = JobUserForm(request.POST, instance = request.user)
        job_profile_form = JobProfileForm(request.POST, instance = request.user.profile)
               
        if job_post_form.is_valid() and job_user_form.is_valid() and job_profile_form.is_valid():
            
            job_post_form.save()
            job_user_form.save()
            job_profile_form.save()

            return HttpResponseRedirect(reverse('thanks'))

    else:
        job_post_form = JobPostForm()
        job_user_form = JobUserForm(instance = request.user)
        job_profile_form = JobProfileForm(instance = request.user.profile)
       

    return render(request, 'job_post_form.html', {'job_post_form': job_post_form, 'job_user_form': job_user_form, 'job_profile_form': job_profile_form})

def thanks(request):
    return HttpResponse("Thanks!")

def job_post_list(request):

    job_posts = JobPost.objects.filter(Q(status='approved') | Q(status='extended')).order_by('-is_verified_sponsor')
    
    return render(request,'job_post_list.html', {'job_posts':job_posts} )
