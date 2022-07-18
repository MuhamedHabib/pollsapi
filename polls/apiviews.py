from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer,\
    VoteSerializer, UserSerializer
from rest_framework import generics, status, viewsets

'''
5.2 Using DRF generic views to simplify code

old method:

class PollList(APIView):
    def get(self, request):
        polls = Poll.objects.all()[:20]
        data = PollSerializer (polls, many=True).data
        return Response(data)
        
        With this change, GET requests to /polls/ and /polls/<pk>/, continue to work as was, but we have a more
        data available with OPTIONS.
        Do an OPTIONs request to /polls/, and you will get a response like this.

'''

'''
generic views tells us:
• Our API now accepts POST
• The required data fields
• The type of each data field.
Pretty nifty! This is what it looks like in Postman.
'''
#### genneric Views:

class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

'''
5.3 More generic views
Let us add the view to create choices and for voting. 
We will look more closely at this code shortly

There is a lot going on here, let us look at the attributes we need to override or set.
• queryset: This determines the initial queryset. The queryset can be further filtered, sliced or ordered by the
view.
• serializer_class: This will be used for validating and deserializing the input and for serializing the
output.
We have used three different classes from rest_framework.generic. The names of the classes are representative of what they do, but lets quickly look at them.
• ListCreateAPIView: Get a list of entities, or create them. Allows GET and POST.
• RetrieveDestroyAPIView: Retrieve an individual entity details, or delete the entity. Allows GET and
DELETE.
• CreateAPIView: Allows creating entities, but not listing them. Allows POST.
'''
'''
We will make changes to ChoiceList and CreateVote,
 because the /polls/ and /polls/<pk> have not changed:
 old ChoiceList:

class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
'''
'''
Just for adding votes (Post only allowed)
'''
'''
old vote method
class CreateVote (generics.CreateAPIView):
    serializer_class = VoteSerializer
'''
'''
5.4 Next Steps
We have working API at this point, but we can simplify our API with a better URL design and remove some code
duplication using viewsets. We will be doing that in the next chapter.
'''
'''
We have three API endpoints
• /polls/ and /polls/<pk>/
• /choices/
• /vote/
'''

'''
6.1 A better URL structure : Important step 
We have three API endpoints
• /polls/ and /polls/<pk>/
• /choices/
• /vote/
They get the work done, but we can make our API more intuitive by nesting them correctly. Our redesigned urls look
like this:
• /polls/ and /polls/<pk>
• /polls/<pk>/choices/ to GET the choices for a specific poll, and to create choices for a specific poll.
(Idenitfied by the <pk>)
• /polls/<pk>/choices/<choice_pk>/vote/ - To vote for the choice identified by <choice_pk>
under poll with <pk>.
'''
class OldChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceList(generics.ListCreateAPIView):
    '''
    From the urls, we pass on pk to ChoiceList. We override the get_queryset method, to filter on choices with
    this poll_id, and let DRF handle the rest.
     '''
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])

        if not request.user == poll.created_by:
           raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    '''
    We pass on poll id and choice id. We subclass this from APIView, rather than a generic view, because we competely
    customize the behaviour. This is similar to our earlier APIView, where in we are passing the data to a serializer, and
    saving or returning an error depending on whether the serializer is valid.
    '''
    serializer_class = VoteSerializer

    def post (self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk,
                'poll': pk,
                'voted_by': voted_by
                }
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])

        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().destroy(request, *args, **kwargs)

'''********************************************************************************************************************************************************************************'''
'''
6.4 Choosing the base class to use
We have seen 4 ways to build API views until now
• Pure Django views
• APIView subclasses
• generics.* subclasses
• viewsets.ModelViewSet
So which one should you use when? My rule of thumb is,
• Use viewsets.ModelViewSet when you are going to allow all or most of CRUD operations on a model.
• Use generics.* when you only want to allow some operations on a model
• Use APIView when you want to completely customize the behaviour.
'''
'''********************************************************************************************************************************************************************************'''

class UserCreate(generics.CreateAPIView):
    '''
    Also, dont forget to give exemption to UserCreate view for authentication by overriding the global setting. The
    UserCreate in polls/apiviews.py should look as follows:
    authentication_classes = ()
    permission_classes = ()
    '''
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

'''
Note the authentication_classes = () and permission_classes = () to exempt UserCreate
from global authentication scheme.
'''

# in apiviews.py
# ...
class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


