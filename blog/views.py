from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login

from . import models
from . import forms

def index(request: HttpRequest):

    num_visits = request.session.get('num_visits', 0)
    num_users = models.CustomUser.objects.all().count()
    num_posts = models.Post.objects.all().count()
    visits_check = (num_visits < 10 or num_visits > 20) and num_visits % 10 in [2,3,4]
    request.session['num_visits'] = num_visits+1
    return render(
        request,
        'blog/index.html',
        context = {
            'num_users': num_users,
            'num_posts': num_posts,
            'num_visits': num_visits,
            'visits_check':visits_check,
        },
    )


class UserDetailView(DetailView):
    model = models.CustomUser
    context_object_name = 'user_detail'
    template_name = 'blog/profile.html'

    slug_field = 'username'


class UserListView(ListView):
    model = models.CustomUser
    context_object_name = 'user_list'
    template_name = 'blog/users.html'

    def get_queryset(self):
        return models.CustomUser.objects.all()

class PostCreateView(CreateView):
    model = models.Post
    template_name = 'blog/create_post.html'
    fields = ['header', 'text']
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.owner = models.CustomUser.objects.get(username=self.request.user.username)
        return super().form_valid(form)
    

class CommentCreateView(CreateView):
    model = models.Comment
    template_name = 'blog/create_comment.html'
    fields = ['text']
    success_url = reverse_lazy('index')
    

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.owner = models.CustomUser.objects.get(username=self.request.user.username)
        fields.post = models.Post.objects.get(id=self.kwargs['pk'])
        fields.save()
        return super().form_valid(form)



class PostDetailView(DetailView):
    model = models.Post
    template_name='blog/comments.html'


class PostDeleteView(DeleteView):
    model = models.Post
    template_name='blog/delete_post.html'
    success_url=reverse_lazy('index')


class CommentDeleteView(DeleteView):
    model = models.Comment
    template_name='blog/delete_comment.html'
    success_url=reverse_lazy('index')



def register(request: HttpRequest):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, "Регистрация прошла успешно")
            return redirect('index')

        # messages.error(request, "Неудачная регистрация. Неправильные данные")
    form = forms.CustomUserCreationForm()
    return render(request, template_name="blog/registration.html", context={"register_form": form})