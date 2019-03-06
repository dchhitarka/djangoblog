
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, EmailPostForm, CommentForm
from django.core.mail import send_mail
# Create your views here.
# CRUD
# CREATE RETRIEVE UPDATE DELETE LIST

def list_view(request):
    query = request.GET.get('q', None)
    qs = Post.objects.all()
    if query is not None:
        qs = Post.objects.filter(Q(title__icontains=query) |
                                 Q(text__icontains=query))
        if not qs:
            messages.success(request, 'No result found! Please try again.')
    context = {
        'qs': qs,
    }
    return render(request, 'blog/list_view.html', context)

@login_required
def detail_delete_view(request, post_id=None):
    obj = get_object_or_404(Post, id=post_id)
    # If url contain delete, then this code is executed
    context = {'obj': obj,}
    if 'delete' in request.path:
        if request.method == 'POST':
            obj.delete()
            messages.success(request, 'Post Deleted Successfully')
            return HttpResponseRedirect('/')
        return render(request, 'blog/delete_view.html', context)
    # Otherwise this code is executed which shows the details of obj
    # For the comment section
    comments = obj.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = obj
            # Save the comment to the database
            new_comment.save()
            return HttpResponseRedirect(f'/{obj.id}/detail/')
    else:
        comment_form = CommentForm()
    context['comments'] = comments
    context['new_comments'] = new_comment
    context['comment_form'] = comment_form
    return render(request, 'blog/detail_view.html', context)

@login_required
def create_update_view(request, post_id=None):
    obj = None
    context = {}
    template = 'blog/create_view.html'
    if post_id is not None:
        template = 'blog/update_view.html'
        obj = get_object_or_404(Post, id=post_id)
        context['obj'] = obj
    form = PostForm(request.POST or None, instance=obj)
    context['form'] = form
    if form.is_valid():
        formobj = form.save(commit=False)
        formobj.save()
        if 'create' in request.path:
            messages.success(request, 'New Post Created Successfully')
            context['form'] = PostForm()
            return HttpResponseRedirect('/')
        else:
            messages.success(request, 'Your Post was Updated Successfully')
            return HttpResponseRedirect(f'/{formobj.id}/detail/')
    return render(request, template, context)

def post_share(request, post_id):
    obj = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj_url = request.build_absolute_uri(obj.get_absolute_url())
            subject = f'{cd["name"]} ({cd["email"]}) recommends you reading {obj.title}'
            message = f'Read {obj.title} at {obj_url}\n\n \'s comments: {cd["comments"]}'
            send_mail(subject, message, 'dchhitarka@gmail.com', [cd['to'],])
            sent = True
            messages.success(request, 'Post shared Successfully')
            return HttpResponseRedirect(obj.get_absolute_url())
    else:
        form = EmailPostForm()
    context = {
        'obj': obj,
        'form': form,
        'sent': sent
    }
    return render(request, 'blog/share.html', context)

# @login_required
# def create_view(request, post_id = None):
#     # obj = get_object_or_404(Post, id=post_id)
#     form = PostForm(request.POST or None)  # , instance=obj)
#     context = {
#         'form': form,
#         # 'obj': obj,
#     }
#     if form.is_valid():
#         formobj = form.save(commit=False)
#         # print(formobj)
#         formobj.save()
#         # print(formobj)
#         messages.success(request, 'New Text Created Successfully')
#         # return HttpResponseRedirect(f'/{formobj.id}/detail/')
#         context = {
#             'form': PostForm()
#         }
#     return render(request, 'blog/create_view.html', context)
#


# def detail_view(request, post_id):
#
#     # try:
#     #     obj = Post.objects.get(id=5)
#     # except:
#     #     raise Http404
#
#
#     # qs = Post.objects.filter(id=5)
#     # if not qs.exist() and qs.count != 1:
#     #     raise Http404
#     # else:
#     #     obj = qs.first()
#
#
#     obj = get_object_or_404(Post, id=post_id)
#     context = {
#         'obj': obj,
#     }
#     return render(request, 'blog/detail_view.html', context)
#
# @login_required
# def update_view(request, post_id):
#     obj = get_object_or_404(Post, id=post_id)
#     form = PostForm(request.POST or None, instance=obj)
#     context = {
#         'form': form,
#
#     }
#     if form.is_valid():
#         formobj = form.save(commit=False)
#         # print(formobj)
#         formobj.save()
#         # print(formobj)
#         messages.success(request, 'New Text Updated Successfully')
#         return HttpResponseRedirect(f'/{formobj.id}/detail/')
#     return render(request, 'blog/update_view.html', context)


# @login_required
# def delete_view(request, post_id):
#     print(request)
#     obj = get_object_or_404(Post, id=post_id)
#     if request.method == 'POST':
#         obj.delete()
#         messages.success(request, 'Post Deleted Successfully')
#         return HttpResponseRedirect('/')
#     context = {
#         'obj': obj,
#     }
#     return render(request, 'blog/delete_view.html', context)

#
# def home(request):
#     response = HttpResponse()
#     response.write("Here's the text of the page")
#     return response


