from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.utils import timezone
from django.views import View

from .models import Question, Answer, Polls, PollsStatistic
from django.shortcuts import render, get_object_or_404


def index(request):
    all_polls = Polls.objects.filter(is_active=True).order_by('-pub_date')
    context = {'all_polls': all_polls, 'user_name': auth.get_user(request).username}
    return render(request, 'polls/index.html', context)


def detail(request, poll_id):
    poll = get_object_or_404(Polls, pk=poll_id)
    questions = poll.question_set.all()

    return render(request, 'polls/detail.html', {'poll': poll,
                                                 'questions': questions,
                                                 'user_name': auth.get_user(request).username})


def results(request, poll_id):
    poll = get_object_or_404(Polls, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll, 'user_name': auth.get_user(request).username})


def vote(request, poll_id):
    poll = get_object_or_404(Polls, pk=poll_id)
    questions = poll.question_set.all()
    for question in questions:
        id = question.id
        try:
            selected_answer = question.answer_set.get(pk=request.POST['answer %s' % id])
        except:
            return render(request, 'polls/detail.html', {
                'poll': poll,
                'questions': questions,
                'user_name': auth.get_user(request).username,
                'error_message': 'Необходим ответ'
            })
        else:
            selected_answer.vote += 1
            selected_answer.save()
    return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))
