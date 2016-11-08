from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Question, Choice


class IndexView(generic.ListView):
  template_name = 'tutorial/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    return Question.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = 'tutorial/detail.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'tutorial/results.html'


def vote(request, pk):
  question = get_object_or_404(Question, pk=pk)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    context = {
      'question': question,
      'error_message': "You didn't select a choice.",
    }
    return render(request, 'tutorial/detail.html', context)
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('tutorial:results', args=(question.id,)))