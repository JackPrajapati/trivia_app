from django.contrib import admin
from .models import GameUser, Answer, Question, GameSummery


class AnswerAdmin(admin.StackedInline):
    can_delete = True
    extra = 1
    model = Answer
    max_num = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
    list_per_page = 10


# Register your models here.
admin.site.register(GameUser)
admin.site.register(Question, QuestionAdmin)
admin.site.register(GameSummery)