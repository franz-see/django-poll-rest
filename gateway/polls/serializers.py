from rest_framework import serializers

from .models import Choice, Question


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'was_published_recently',
                  'choices', ]
