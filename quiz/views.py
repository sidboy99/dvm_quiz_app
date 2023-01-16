from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Quiz, QuizAttempt, Question, Attempt, question_options_list
from .forms import QuizTakerForm
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponse
from django.forms import formset_factory


def show_question_form(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if len(QuizAttempt.objects.filter(quiz=quiz, user=request.user)) == 0:
        quiz_attempt = QuizAttempt()
        quiz_attempt.quiz = quiz
        quiz_attempt.user = request.user
        quiz_attempt.save()
    else:
        quiz_attempt = QuizAttempt.objects.filter(quiz=quiz, user=request.user).last()

    questions_list = Question.objects.filter(quiz=quiz)
    q_a_list = question_options_list(quiz)
    QuizFormSet = formset_factory(QuizTakerForm, extra=len(questions_list))

    if request.method =='POST':
        formset = QuizFormSet(request.POST)
        current_attempt = quiz_attempt.no_of_attempts + 1
        i = 0
        for dict_ in formset.cleaned_data:
            loc = i
            attempt = Attempt.objects.create(chosen=dict_['chosen'], que=questions_list[loc],
                                             attempted_by=request.user, quiz=quiz_attempt, attempt_no=current_attempt)
            attempt.save()
            i += 1

        quiz_attempt.score = 0
        for attempt in Attempt.objects.filter(quiz=quiz_attempt):
            if (attempt.chosen == attempt.que.ans) and (attempt.attempt_no == current_attempt):
                quiz_attempt.score += 1
        quiz_attempt.no_of_attempts += 1
        quiz.save()
        quiz_attempt.save()
        return HttpResponse(f'Quiz score : {quiz_attempt.score}')
    
    formset = QuizFormSet()
    zipped_list = list(zip(q_a_list, formset))

    return render(request, 'quiz/quiz_form.html', {'zipped_list':zipped_list, 'formset':formset})


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/home.html'
    context_object_name = 'quizzes'