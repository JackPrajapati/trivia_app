from django.db import models
from model_utils.models import TimeStampedModel


# game user model
class GameUser(TimeStampedModel):
    gameuser = models.CharField(blank=False, null=False, unique=True, max_length=255)

    def __str__(self):
        return str(self.gameuser)


# game question model
class Question(TimeStampedModel):
    QUESTION_TYPE = (
        ('', '---'),
        ('radio', 'RADIO'),
        ('checkbox', 'CHECKBOX'),
    )
    question = models.TextField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    question_type = models.CharField(blank=True, null=True, choices=QUESTION_TYPE, default='', max_length=255)

    class Meta:
        verbose_name = "Question Answer"

    def __str__(self):
        return str(self.question)


# game answer model
class Answer(TimeStampedModel):
    option = models.CharField(blank=True, null=True, max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Answer Model"

    def __str__(self):
        return str(self.option)


class GameSummery(TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    gameuser = models.ForeignKey(GameUser, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Game Summery"
        unique_together = ('question', 'gameuser')

    def __str__(self):
        return str(self.gameuser) + " - " + str(self.question) + " - " + str(self.answers)
