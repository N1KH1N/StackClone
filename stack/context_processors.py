from stack.models import Questions,Answers


def activities(request):
    if request.user.is_authenticated:
        cnt=Questions.objects.filter(user=request.user).count
        acnt=Answers.objects.filter(user=request.user).count
        return {"qcount":cnt,"acount":acnt}
    else:
        return {"qcount":0}

