from django.conf import settings
from django.db import models

# 게시물(Post) 테이블 생성
class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='작성자')
	title = models.CharField(max_length=200, verbose_name='제목')
	content = models.TextField(verbose_name='내용')
	image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name='사진')
	tech_stack = models.CharField(max_length=200, blank=True, verbose_name='기술 스택')
	github_link = models.CharField(max_length=300, blank=True, verbose_name='깃허브 링크')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

	def __str__(self):
		return f"{self.title} - {self.author}"
