from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Like, Comment
from .serializers import PostSerializer

def home_view(request):
    posts = Post.objects.all().prefetch_related('comments', 'likes')
    return render(request, 'posts/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            Post.objects.create(
                user=request.user,
                title=title,
                content=content
            )
            messages.success(request, 'Post created successfully!')
        else:
            messages.error(request, 'Title and content are required.')
    
    return redirect('home')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, 'Post updated successfully!')
        else:
            messages.error(request, 'Title and content are required.')
    
    return redirect('home')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
    
    return JsonResponse({
        'liked': created,
        'total_likes': post.likes.count()
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    
    if content:
        Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )
    
    return redirect('home')

def profile_view(request):
    total_likes = sum(post.likes.count() for post in request.user.posts.all())
    return render(request, 'accounts/profile.html', {'total_likes': total_likes})