from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import LoginForm, QuestionnaireForm
from .models import Questionnaire


#class IndexView(generic.base.TemplateView):
#  template_name = 'survey/index.html'
def index_view(request):
  user = request.user
  responded = False
  if user and user.is_authenticated():
    responded = Questionnaire.objects.filter(user=user).exists()

  context = { 'responded': responded }
  return render(request, 'survey/index.html', context)


@login_required(login_url=reverse_lazy('survey:login'))
def edit_view(request):
  user = request.user
  
  if not request.method == 'POST':
    if Questionnaire.objects.filter(user=user).exists():
      q = Questionnaire.objects.get(user=user)
      form = QuestionnaireForm(instance=q)
    else:
      form = QuestionnaireForm()
    context = { 'form': form }
    return render(request, 'survey/edit.html', context)

  if Questionnaire.objects.filter(user=user).exists():
    q = Questionnaire.objects.get(user=user)
    form = QuestionnaireForm(request.POST, instance=q)
  else:
    form = QuestionnaireForm(request.POST)
  print(form.__dict__)
  print(form.errors)
  if form.is_valid():
    q = form.save(commit=False)
    q.user = request.user
    q.save()
    return HttpResponseRedirect(reverse('survey:index'))
  else:
    context = { 'form': form }
    return render(request, 'survey/edit.html', context)

  

def login_view(request):
  if not request.method == 'POST':
    form = LoginForm()
    context = {'form': form}
    return render(request, 'survey/login.html', context)

  form = LoginForm(request.POST)
  if not form.is_valid():
    context = { 'form': form }
    return render(request, 'survey/login.html', context)
  username = form.cleaned_data['username']
  password = form.cleaned_data['password']
  user = authenticate(username=username, password=password)
  login(request, user)
  return HttpResponseRedirect(reverse('survey:index'))


@login_required(login_url=reverse_lazy('survey:login'))
def logout_view(require):
  logout(require)
  return HttpResponseRedirect(reverse('survey:index'))
