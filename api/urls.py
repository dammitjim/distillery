from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    url(r'^distilleries/$', views.DistilleryList.as_view(), name="distillery-list")
]

urlpatterns = format_suffix_patterns(urlpatterns)