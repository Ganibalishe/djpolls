from django.contrib import admin
from .models import Question, Answer, Polls, PollsStatistic, PollsStatisticAdmin, UserResponses


def all_polls(modeladmin, reguest, queryset):
    for qs in queryset:
        print(qs.poll_title)


def complete_poll(modeladmin, reguest, queryset):
    queryset.update(is_active=True)


complete_poll.short_description = 'Опубликовать новости'


def incomplete_poll(modeladmin, reguest, queryset):
    queryset.update(is_active=False)


incomplete_poll.short_description = 'Снять с публикации'


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 2


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


class PollsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['poll_title', 'is_active']}
         ),
        ('Информация о дате',
         {'fields': ['pub_date'],
          'classes': ['collapse']}
         ),
        ('Прошедшие опрос:',
         {'fields': ['users']}
         ),
    ]
    actions = [all_polls, complete_poll, incomplete_poll]
    inlines = [QuestionInLine]


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['poll', 'question_text']}
         ),
        ('Ответившие на вопрос:',
         {'fields': ['users']}
         ),
    ]
    inlines = [AnswerInline]


admin.site.register(UserResponses)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Polls, PollsAdmin)
admin.site.register(PollsStatistic, PollsStatisticAdmin)
