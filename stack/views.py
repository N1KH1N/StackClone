from django.shortcuts import render,redirect
from stack.forms import RegistrationForm,LoginForm,QuestionForm,UserProfileForm
from django.views.generic import View,CreateView,FormView,TemplateView,ListView,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from stack.models import Questions,Answers,UserProfile
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

# Create your views here.


# class SignUpView(View):
    # def get(self,request,*args,**kwargs):
    #     form=RegistrationForm()
    #     return render(request,"register.html",{"form":form})
    
    # def post(self,request,*args,**kwargs):
    #     form=RegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("register")
    #     else:
    #         return render(request,"register.html",{"form":form})

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
decs=[signin_required,never_cache]



class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("register")

        
        
# class SignInView(View):
#     def get(self,request,*args,**kwargs):
#         form=LoginForm()
#         return render(request,"login.html",{"form":form})
#     def post(self,request,*args,**kwargs):
#         form=LoginForm(request.POST)
#         uname=form.cleaned_data.get("username")
#         psd=form.cleaned_data.get("password")
#         print("uname","psd")
#         usr=authenticate(request,username=uname,password=psd)
#         if usr:
#             login(request,usr)
#             return redirect()
#         else:
#             return render(request,"login.html",{"form":form})

class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            psd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=psd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":self.form_class})


class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    model=Questions
    form_class=QuestionForm
    template_name="index.html"
    success_url=reverse_lazy("home")
    context_object_name="questions"

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        return Questions.objects.all().order_by("-created_date")
    
    
@method_decorator(decs,name="dispatch")
class AddAnswerView(View):
    def post(self,request,*args,**kwargs):
        qid=kwargs.get("id")
        ques=Questions.objects.get(id=qid)
        usr=request.user
        ans=request.POST.get("answer")
        Answers.objects.create(user=usr,question=ques,answer=ans)
        return redirect("home")
    
@method_decorator(decs,name="dispatch")
class UpVoteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        ans=Answers.objects.get(id=id)
        ans.up_vote.add(request.user)
        ans.save()
        return redirect("home")
    

@method_decorator(decs,name="dispatch")
class UpVoteRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        ans=Answers.objects.get(id=id)
        ans.up_vote.remove(request.user)
        ans.save()
        return redirect("home")

    
@method_decorator(decs,name="dispatch")
class UserProfileCreateView(CreateView):
    form_class=UserProfileForm
    template_name="profile-add.html"
    model=UserProfile
    success_url=reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

@method_decorator(decs,name="dispatch")
class ProfileDetailView(TemplateView):
    template_name="profile-detail.html"


@method_decorator(decs,name="dispatch")
class ProfileUpdateView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"

@method_decorator(decs,name="dispatch")
class QuestionDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Questions.objects.get(id=id).delete()
        return redirect("home")
    
