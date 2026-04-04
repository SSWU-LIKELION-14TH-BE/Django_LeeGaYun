from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Comment

@login_required
def post_create_view(request):
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'post_create.html', {'form': form})

def post_detail_view(request, pk):
	post = get_object_or_404(Post, pk=pk)
	comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_at')
	comment_form = CommentForm()

	# 댓글/대댓글 작성 처리
	if request.method == 'POST' and 'comment_submit' in request.POST:
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.author = request.user
			parent_id = request.POST.get('parent_id')
			if parent_id:
				try:
					parent_comment = Comment.objects.get(id=parent_id, post=post)
					new_comment.parent = parent_comment
				except Comment.DoesNotExist:
					new_comment.parent = None
			new_comment.save()
			return redirect('post_detail', pk=post.pk)

	return render(request, 'post_detail.html', {
		'post': post,
		'comments': comments,
		'comment_form': comment_form,
	})

# 좋아요 처리 뷰
@login_required
def post_like_view(request, pk):
	post = get_object_or_404(Post, pk=pk)
	user = request.user
	if user in post.likes.all():
		post.likes.remove(user)
	else:
		post.likes.add(user)
	return HttpResponseRedirect(reverse('post_detail', args=[pk]))

# 댓글 좋아요 처리 뷰
@login_required
def comment_like_view(request, comment_id):
	comment = get_object_or_404(Comment, id=comment_id)
	user = request.user
	if user in comment.likes.all():
		comment.likes.remove(user)
	else:
		comment.likes.add(user)
	return redirect('post_detail', pk=comment.post.pk)
