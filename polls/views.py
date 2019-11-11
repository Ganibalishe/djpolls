from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.utils import timezone
from django.views import View
from .models import Question, Answer, Polls, PollsStatistic
from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    all_polls = Polls.objects.filter(is_active=True).order_by('-pub_date')
    context = {'all_polls': all_polls, 'user_name': auth.get_user(request).username}
    return render(request, 'polls/index.html', context)


def detail(request, poll_id):
    poll = get_object_or_404(Polls, pk=poll_id)
    question = poll.question_set.all()[0]
    if auth.get_user(request).username in poll.users:
        return redirect('/polls/passed')
    else:
        for q in poll.question_set.all().order_by('question_text'):
            if auth.get_user(request).username not in q.users:
                question = q
                break
        return render(request, 'polls/detail.html', {'poll': poll,
                                                     'question': question,
                                                     'user_name': auth.get_user(request).username})


def results(request, poll_id):
    poll = get_object_or_404(Polls, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll, 'user_name': auth.get_user(request).username})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    poll = get_object_or_404(Polls, pk=question.poll.id)
    questions_queryset = poll.question_set.all().order_by('question_text')

    try:
        selected_answer = question.answer_set.get(pk=request.POST['answer %s' % question_id])
    except:
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'question': question,
            'user_name': auth.get_user(request).username,
            'error_message': 'Необходим ответ'
        })
    else:
        selected_answer.vote += 1
        selected_answer.save()

    last_question = questions_queryset[len(questions_queryset) - 1]
    questions_list = list(questions_queryset)
    print(last_question)
    print(question)

    if question.question_text != last_question.question_text:
        question.users.append(auth.get_user(request).username)
        question.save()
        return render(request, 'polls/detail.html', {'poll': poll,
                                                     'question': questions_list[questions_list.index(question) + 1],
                                                     'user_name': auth.get_user(request).username})
    else:
        question.users.append(auth.get_user(request).username)
        question.save()
        poll.users.append(auth.get_user(request).username)
        poll.save()
        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))


def passed(request):
    all_polls = Polls.objects.filter(is_active=True).order_by('-pub_date')
    context = {'all_polls': all_polls, 'user_name': auth.get_user(request).username}
    return render(request, 'polls/passed.html', context)
