from datetime import datetime
from django.shortcuts import render
from django.views import View
from .models import GameUser, Question, Answer, GameSummery


class Index(View):
    '''
    Index page to start the question and answers.
    '''

    def get(self, request):
        '''
        Get method to start the application index page.
        '''
        # get the question sequence
        que_sequence = request.GET.get('que_sequence', None)
        if que_sequence:
            # if question sequence is available then provide the requested question
            question = Question.objects.get(sequence=que_sequence)
        else:
            # else start the game
            question = Question.objects.get(sequence=1)
        context = {
            'splash': True,
            'next': True,
            'question': question
        }
        return render(request, 'trivia_app/index.html', context)


    def post(self, request):
        '''
        Post method to save and display the data.
        '''
        # get the submitted data
        data = request.POST.dict()
        # get the user requesting
        game_username = data.get('game_username', '')
        # get the question sequence
        que_sequence = data.get('que_sequence', '')
        # get the user or create
        user, created = GameUser.objects.get_or_create(gameuser=game_username)
        context = {
            'game_username': user.gameuser,
        }
        # if all questions are done or not
        # save the data in summery
        radio_ans = data.get('radios', None)
        checkbox_ans = [ v for k,v in data.items() if 'checkboxs_' in k]
        # get the current question
        current_que = Question.objects.get(sequence=int(que_sequence))
        answers = None
        if radio_ans:
            answers = Answer.objects.filter(id=radio_ans)
        elif len(checkbox_ans):
            answers = Answer.objects.filter(id__in=checkbox_ans)
        if answers:
            if len(answers) == 1:
                try:
                    GameSummery.objects.get_or_create(
                        question=current_que,
                        answers=answers.first(),
                        gameuser=user,
                    )
                except:
                    GameSummery.objects.create(
                        question=current_que,
                        answers=answers.first(),
                        gameuser=user,
                    )
            else:
                for opt in answers:
                    try:
                        GameSummery.objects.get_or_create(
                            question=current_que,
                            answers=opt,
                            gameuser=user,
                        )
                    except:
                        GameSummery.objects.create(
                            question=current_que,
                            answers=opt,
                            gameuser=user,
                        )
        next_que = Question.objects.filter(sequence=int(que_sequence) + 1)
        # if next question to ask
        if next_que.exists() and len(next_que) == 1:
            context.update({'question': next_que.first(), 'next': True})
        # else show summery
        else:
            # get the user answers and questions
            gamesummery = GameSummery.objects.filter(gameuser=user)
            # get the radio answers
            radio_que = Question.objects.get(sequence=2)
            # get the check-box answers
            checkbox_que = Question.objects.get(sequence=3)
            summery_list = list()
            # prepare the data to display
            # append radio answers
            summery_list.extend([{radio_que.question :summery_answers.answers.option for summery_answers in gamesummery.filter(question=radio_que)}])
            # append check-box answers
            summery_list.extend([{
                checkbox_que.question:', '.join([summery_answers.answers.option for summery_answers in gamesummery.filter(question=checkbox_que)]),
            }])
            # update the context
            context.update({
                'summery': summery_list,
                'date': datetime.strftime(gamesummery.latest('id').answers.created,"%dth %B %I:%M %p"),
                })
        return render(request, 'trivia_app/index.html', context)
