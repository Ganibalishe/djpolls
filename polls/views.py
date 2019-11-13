from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from .models import Question, Polls, UserResponses
from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    all_polls = Polls.objects.filter(is_active=True).order_by('-pub_date')
    all_user_responses = UserResponses.objects.all()
    context = {'all_polls': all_polls,
               'user_name': auth.get_user(request).username,
               'all_user_responses': all_user_responses}

    return render(request, 'polls/index.html', context)


def detail(request, poll_id):
    poll = get_object_or_404(Polls, pk=poll_id)

    for q in poll.question_set.all().order_by('question_text'):
        user_responses = UserResponses.objects.filter(user=auth.get_user(request), question=q)

        if len(user_responses) > 0:
            continue
        else:
            question = q
            return render(request, 'polls/detail.html', {'poll': poll,
                                                         'question': question,
                                                         'user_name': auth.get_user(request).username})
    return redirect('/polls/passed')


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

    if question.question_text != last_question.question_text:
        user_responses = UserResponses(user=auth.get_user(request), poll=poll, question=question, answer=selected_answer)
        user_responses.save()
        return render(request, 'polls/detail.html', {'poll': poll,
                                                     'question': questions_list[questions_list.index(question) + 1],
                                                     'user_name': auth.get_user(request).username})
    else:
        user_responses = UserResponses(user=auth.get_user(request),poll=poll, question=question, answer=selected_answer)
        user_responses.save()
        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))


def passed(request):
    all_polls = Polls.objects.filter(is_active=True).order_by('-pub_date')
    context = {'all_polls': all_polls, 'user_name': auth.get_user(request).username}
    return render(request, 'polls/passed.html', context)
