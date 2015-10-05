from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


# 用户
class User(AbstractUser):
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    weight = models.IntegerField(default=10, verbose_name='标签大小')

    @models.permalink
    def get_absolute_url(self):
        return ('tag', (), {
            'tag': self.name
        }
        )

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


# 文章分类
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField('显示顺序(从小到大)', default=999)

    @models.permalink
    def get_absolute_url(self):
        return ('category', (), {
            'category': self.name,
        }
        )

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = RichTextUploadingField(config_name='default', verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户')
    category = models.ForeignKey(Category, blank=False, null=False, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    @models.permalink
    def get_absolute_url(self):
        return ('article_content', (), {
            'title': self.title,
        }
        )

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title


# 留言
class Message(models.Model):
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    content = models.TextField(verbose_name='留言内容', max_length=150)
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return str(self.id)




