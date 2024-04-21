from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Job, JobApplication


class HomeView(ListView):
    template_name = "core/home.html"
    context_object_name = "jobs"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Job.objects.exclude(job_applications__user=self.request.user)
        else:
            return Job.objects.all()


class JobDetailView(DetailView):
    template_name = "core/job_detail.html"
    queryset = Job.objects.all()
    context_object_name = "job"


@method_decorator(login_required, name="dispatch")
class JobApplyConfirm(DetailView):
    template_name = "core/job_apply_confirm.html"
    queryset = Job.objects.all()
    context_object_name = "job"


@method_decorator(login_required, name="dispatch")
class JobApply(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        job = get_object_or_404(Job, id=kwargs["pk"])
        try:
            profile = user.userprofile
        except:
            messages.error(self.request, "Please complete your profile !")
            return redirect("home")
        if not profile.resume:
            messages.error(self.request, "Please add your resume before applying for a job !")
            return redirect("home")
        JobApplication.objects.update_or_create(user=user, job=job, defaults={"status": "APPLIED"})
        messages.success(self.request, "Successfully applied to the job !")
        return redirect("home")


@method_decorator(login_required, name="dispatch")
class MyJobView(ListView):
    template_name = "core/my_jobs.html"
    context_object_name = "my_jobs"

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
