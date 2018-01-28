from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from .forms import PostForm, CommentForm, RegistrationForm
from .models import Post


def post_list(request):
    return render(request, 'posts/post_list.html',
                  {'posts': Post.objects.all().order_by('-id')})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = None
    if request.user.is_authenticated:
        comment_form = CommentForm(request.POST or None)
    if comment_form and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    comments = post.comment_set.all().order_by('-id')
    return render(request, 'posts/post_detail.html',
                  {'post': post, 'comments': comments,
                   'comment_form': comment_form})


def post_tagged(request, tag):
    return render(request, 'posts/post_list.html',
                  {'posts':
                   Post.objects.filter(tags__name__in=[tag]).order_by('-id')})


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect(instance)
    return render(request, 'posts/post_form.html', {'form': form})


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = 'accounts:register-done'
    model = User

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(User.objects.make_random_password())
        obj.save()

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        opts = {
            'use_https': self.request.is_secure(),
            'request': self.request,
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        messages.success(self.request,
                         'Check your email for verification letter.')
        return redirect('/')
