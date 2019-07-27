from django.conf.urls import include, url

from rest_framework import routers

from . import views

routeList = [
    (r'choices', views.ChoiceViewSet),
    (r'questions', views.QuestionViewSet),
]

router = routers.DefaultRouter()
for route in routeList:
    router.register(route[0], route[1])

app_name = 'polls'
urlpatterns = [
    url(r'^', include(router.urls)),
]
