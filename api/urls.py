from django.conf.urls import url
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

NAMESPACE = "api"
DISTILLERY_LIST_NAME = "distillery-list"
DISTILLERY_DETAIL_NAME = "distillery-detail"


def get_url_name(name):
    return "{namespace}:{name}".format(namespace=NAMESPACE, name=name)


@api_view(['GET'])
def index(request, format=None):
    return Response({
        "distilleries": reverse(get_url_name(DISTILLERY_LIST_NAME), request=request, format=format),
    })
    pass

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^distilleries/$', views.DistilleryList.as_view(), name=DISTILLERY_LIST_NAME),
    url(r'^distilleries/(?P<pk>[0-9]+)/$', views.DistilleryDetail.as_view(), name=DISTILLERY_DETAIL_NAME),
]

urlpatterns = format_suffix_patterns(urlpatterns)
