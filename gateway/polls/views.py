from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import response, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .serializers import ChoiceSerializer, QuestionSerializer
from .models import Choice, Question


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        includeFuture = self.request.query_params.get(
            'includeFuture', 'false').lower() == 'true'
        queryset = Question.objects.all()
        if not includeFuture:
            queryset = queryset.filter(pub_date__lte=timezone.now())

        return queryset.order_by('-pub_date')

    @action(methods=['post'], detail=True, permission_classes=[AllowAny])
    def vote(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        try:
            choice = request.data['choice']
        except KeyError:
            return HttpResponseBadRequest('No choice provided')
        try:
            selected_choice = question.choices.get(pk=choice)
        except Choice.DoesNotExist:
            return HttpResponseBadRequest('Unknown choice %s' % choice)
        else:
            selected_choice.votes += 1
            selected_choice.save()
            serializer = self.get_serializer(question)
            return response.Response(serializer.data)
