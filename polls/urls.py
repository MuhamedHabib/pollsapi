'''
Our API will have two endpoints returning data in JSON format.
• /polls/ GETs list of Poll
• /polls/<id>/ GETs data of a specific Poll
'''
#from .views import *
from polls.views import polls_list, polls_detail
from django.urls import path

from rest_framework.authtoken import views
from .apiviews import *
from rest_framework.routers import DefaultRouter
from .apiviews import PollViewSet

'''
Our urls are looking good, and we have a views with very little code duplication, but we can do better.
The /polls-api-view/ and /polls-api-view/<pk>/ urls require two view classes, with the same serializer and base queryset. We
can group them into a viewset, and connect them to the urls using a router.
This is what it will look like:
'''
router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

urlpatterns=[
    #path("polls/", polls_list, name ="polls_list"),
    #path("polls/<int:pk>", polls_detail, name="polls_detail"),
    path("polls-api-view/", PollList.as_view(), name="polls_list2"),
    path("polls-api-view/<int:pk>/", PollDetail.as_view(), name="polls_detail"),
    path("choices/", OldChoiceList.as_view(), name="choice_list1"),
    path("vote/", CreateVote.as_view(), name="create_vote"),
    path("polls-api-view/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path("polls-api-view/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    #path("login/", views.obtain_auth_token, name="login"),
]
urlpatterns += router.urls


