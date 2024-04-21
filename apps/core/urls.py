from django.urls import path
from .views import HomeView, JobDetailView, JobApplyConfirm, JobApply, MyJobView, ContactView

urlpatterns = [
    path('job/<int:pk>/', JobDetailView.as_view(), name="job_detail"),
    path("job/apply-confirm/<int:pk>/", JobApplyConfirm.as_view(), name="apply_confirm"),
    path("job/apply/<int:pk>/", JobApply.as_view(), name="job_apply"),
    path("my-jobs/", MyJobView.as_view(), name="my_jobs"),
    path("contact/", ContactView.as_view(), name="contact"),
    path('', HomeView.as_view(), name='home')
]
