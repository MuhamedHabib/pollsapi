'''
We will use ModelSerializer which will reduce
code duplication by automatically determing the set of fields and by creating implementations of the create() and
update() methods.
'''
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Poll, Choice, Vote
from django.contrib.auth.models import User

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)
    class Meta:
        model = Choice
        fields='__all__'

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)
    class Meta:
        model=Poll
        fields= '__all__'

'''
What have we got with this? The PollSerializer class has a number of methods,
• A is_valid(self, ..) method which can tell if the data is sufficient and valid to create/update a model
instance.
• A save(self, ..) method, which knows how to create or update an instance.
• A create(self, validated_data, ..) method which knows how to create an instance. This method
can be overriden to customize the create behaviour.
• A update(self, instance, validated_data, ..) method which knows how to update an instance. This method can be
 overriden to customize the update behaviour.
'''

'''
TEST SERIALIZER :
Let’s use the serializer to create a Poll object.
In [1]: from polls.serializers import PollSerializer
In [2]: from polls.models import Poll
In [3]: poll_serializer = PollSerializer(data={"question": "Mojito or Caipirinha?",
˓→"created_by": 1})
In [4]: poll_serializer.is_valid()
Out[4]: True
In [5]: poll = poll_serializer.save()
In [6]: poll.pk
Out[6]: 5

ps: The poll.pk line tells us that the object has been commited to the DB. You can also use the serializer to update a
Poll object.
'''

'''
UPDATE OBJECT:
In [9]: poll_serializer = PollSerializer(instance=poll, data={"question": "Mojito,
˓→Caipirinha or margarita?", "created_by": 1})
In [10]: poll_serializer.is_valid()
Out[10]: True
In [11]: poll_serializer.save()
Out[11]: <Poll: Mojito, Caipirinha or margarita?>
In [12]: Poll.objects.get(pk=5).question
Out[12]: 'updated_Question??'
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs= {'password': {'write_only': True}}
        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            '''
            We want to ensure that tokens are created when user is created in UserCreate view, so we update the
            UserSerializer. Change your serializers.py by adding this line
            '''
            Token.objects.create(user=user)
            return user

        '''
        We have overriden above (UserSerializer) the ModelSerializer method’s create() to save the User instances. We ensure that we set
        the password correctly using user.set_password, rather than setting the raw password as the hash. We also
        don’t want to get back the password in response which we ensure using extra_kwargs = {'password':
        {'write_only': True}}.
        '''
