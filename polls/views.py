from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Poll
from rest_framework.exceptions import PermissionDenied

# Create your views here.
'''
Write two place holder view functions and connect them in your urls.py. We will finish polls_list and
polls_detail shortly.
'''

def polls_list(request):
    MAX_OBJECTS = 20
    polls = Poll.objects.all()[:MAX_OBJECTS]
    data = {"results": list(polls.values("question", "created_by__username", "pub_date"))}
    return JsonResponse(data)

'''
A JsonResponse is
a like HttpResponse with content-type=application/json.
Similarly, polls_detail gets a specific Poll using get_object_or_404(Poll, pk=pk), and returns it wrapped
in JsonResponse
'''
def polls_detail(request,pk):
    poll = get_object_or_404(Poll, pk=pk)
    data = {"results": {
        "question" : poll.question,
        "created_by" : poll.created_by.username,
        "pub_date" : poll.pub_date
    }}
    return JsonResponse(data)

'''
3.5 Why do we need DRF?
(DRF = Django Rest Framework)
We were able to build the API with just Django, without using DRF, so why do we need DRF? Almost always, you
will need common tasks with your APIs, such as access control, serialization, rate limiting and more.
DRF provides a well thought out set of base components and convenient hook points for building APIs. We will be
using DRF in the rest of the chapters.
'''

'''
href=https://buildmedia.readthedocs.org/media/pdf/djangoapibook/latest/djangoapibook.pdf
4.1 Serialization and Deserialization
The first thing we need for our API is to provide a way to serialize model instances into representations. Serialization is
the process of making a streamable representation of the data which we can transfer over the network. Deserialization
is its reverse process.
'''


