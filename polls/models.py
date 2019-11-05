from django.contrib import admin
from django.db import models
from django.utils import timezone


class Polls(models.Model):
    poll_title = models.CharField(max_length=100, verbose_name='Опрос')
    pub_date = models.DateTimeField('Дата')
    is_active = models.BooleanField(verbose_name="Опубликован")

    def __str__(self):
        return self.poll_title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Вопрос')
    poll = models.ForeignKey(Polls, on_delete=models.CASCADE, verbose_name='Опрос')

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    answer_text = models.CharField(max_length=200, verbose_name='Ответ')
    vote = models.IntegerField(default=0, verbose_name='Кол-во ответов')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class PollsStatistic(models.Model):
    class Meta:
        db_table = "PollsStatistic"

    poll = models.ForeignKey(Polls, on_delete=models.CASCADE)
    date = models.DateField('Дата', default=timezone.now)
    answer = models.IntegerField('Ответы', default=0)

    def __str__(self):
        return self.poll.poll_title


class PollsStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'answer')
    search_fields = ('__str__',)
