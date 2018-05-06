#-*- coding:utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from wmd import models as wmd_models        # 导入wmd的models
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import markdown

class Category(models.Model):
    name=models.CharField(max_length=80)
    sortnum=models.IntegerField(default=10)
    articles=models.IntegerField(default=0)
    user_id=models.IntegerField(default=0)

class Article(models.Model):
    channel1_id=models.IntegerField(default=0)
    channel2_id=models.IntegerField(default=0)
    category=models.ForeignKey(Category)
    title=models.CharField(max_length=200)
    pic=models.CharField(max_length=80)
    tags=models.CharField(max_length=120)
    summary=models.CharField(max_length=500)
    content=models.TextField()
    createtime=models.DateTimeField(default="0000-00-00 00:00:00")
    views=models.IntegerField(default=0)
    comments=models.IntegerField(default=0)
    goods=models.IntegerField(default=0)
    bads=models.IntegerField(default=0)
    status=models.IntegerField(default=1)       #1发布；0草稿
    user_id=models.IntegerField(default=1)
    username=models.CharField(max_length=80)
    ishome=models.IntegerField(default=0)       #1发布；0草稿
    isrecommend=models.IntegerField(default=0)       #1发布；0草稿
    istop=models.IntegerField(default=0)       #1发布；0草稿
    isoriginal=models.IntegerField(default=1)       #1发布；0草稿
    cancomment=models.IntegerField(default=1)       #1发布；0草稿
    password=models.CharField(max_length=80)       #1发布；0草稿

class Comment(models.Model):
    article=models.ForeignKey(Article)
    user_id=models.IntegerField(default=0)
    username=models.CharField(max_length=80)
    content=models.TextField()
    createtime=models.DateTimeField(default="0000-00-00 00:00:00")
    goods=models.IntegerField(default=0)
    bads=models.IntegerField(default=0)
    reply_id=models.IntegerField(default=0)
    
  
class UserProfile(models.Model):
    user=models.ForeignKey(User,unique=True)
    #头像
    avatar=models.ImageField(upload_to='avatar')

    #基本信息
    nickname=models.CharField(max_length=80)
    realname=models.CharField(max_length=80)
    gender=models.IntegerField(default=0)
    birthday=models.DateTimeField(default=datetime.datetime.now())
    birthcity=models.CharField(max_length=80)
    residecity=models.CharField(max_length=80)

    #个人信息
    affectivestatus=models.IntegerField(default=0)
    lookingfor=models.IntegerField(default=0)
    bloodtype=models.IntegerField(default=0)
    site=models.CharField(max_length=80)
    bio=models.CharField(max_length=255)
    interest=models.CharField(max_length=255)
    sightml=models.CharField(max_length=255)
    timeoffset=models.CharField(max_length=80)
   
    #联系方式
    qq=models.CharField(max_length=80)
    msn=models.CharField(max_length=80)
    taobao=models.CharField(max_length=80)
    email=models.CharField(max_length=80)
    phone=models.CharField(max_length=80)
    mobile=models.CharField(max_length=80)
    address=models.CharField(max_length=80)
    zipcode=models.CharField(max_length=80)

class Blog(models.Model):
    user_id=models.IntegerField(default=0)
    domain=models.CharField(max_length=200)
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    keywords=models.CharField(max_length=200)
    about=models.CharField(max_length=500)
    announcement=models.CharField(max_length=500)
    modules=models.CharField(max_length=200)
    template=models.CharField(max_length=50)
    css=models.CharField(max_length=500)
    headhtml=models.CharField(max_length=500)
    footerhtml=models.CharField(max_length=500)
    todayviews=models.IntegerField(default=0)
    totalviews=models.IntegerField(default=0)
    articles=models.IntegerField(default=0)
    comments=models.IntegerField(default=0)
    createtime=models.DateTimeField(default=datetime.datetime.now())

class Channel(models.Model):
    parent_id=models.IntegerField(default=0)
    name=models.CharField(max_length=80)
    sortnum=models.IntegerField(default=10)
    articles=models.IntegerField(default=0)
    users=models.IntegerField(default=0)
    user_id=models.IntegerField(default=0)
    username=models.CharField(max_length=80)
    isenable=models.IntegerField(default=1)


class Type(models.Model):
    """分类"""
    name = models.CharField(max_length=50)
    add_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def getCount(self):
        """获取数目"""
        return Blog.objects.filter(type=self.id).count()

    class Meta:
        db_table = 'type'


class Blog(models.Model):
    title = models.CharField(max_length=100)
    type = models.IntegerField(default=0)
    img = models.CharField(max_length=500, null=True)  # 博客导图
    summary = models.CharField(max_length=500, null=True)
    rss = models.CharField(max_length=1024, null=True)  # 订阅源
    content = wmd_models.MarkDownField()
    content_show = wmd_models.MarkDownField(u'正文显示', null=True)
    add_date = models.DateTimeField()
    counts = models.IntegerField(default=0)  # 点击率
    is_show = models.CharField(max_length=100, null=True)  # 加密

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        self.content_show = mark_safe(
            markdown.markdown(force_unicode(self.content), ['codehilite'], safe_mode='escape'))
        super(Blog, self).save()

    class Meta:
        db_table = 'blog'

    def getType(self):
        """获取类型"""
        return Type.objects.get(pk=self.type)

    def getTags(self):
        """获取标签"""
        return BlogTag.objects.filter(blog=self.id)


class Tag(models.Model):
    """个人标签"""
    name = models.CharField(max_length=100)
    add_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'tags'


class BlogTag(models.Model):
    """主题标签"""
    blog = models.ForeignKey(Blog)
    tag = models.ForeignKey(Tag)
    add_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.tag.name

    class Meta:
        db_table = 'blog_tag'


class WikiType(models.Model):
    """wiki分类"""
    name = models.CharField(max_length=50)
    add_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def getCount(self):
        """获取数目"""
        return Wiki.objects.filter(category=self.id).count()

    class Meta:
        db_table = 'wiki_type'


class Wiki(models.Model):
    """WIki"""
    category = models.IntegerField()
    content = wmd_models.MarkDownField()
    content_show = wmd_models.MarkDownField(u'show', null=True)
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        db_table = 'wiki'

    def save(self, force_insert=False, force_update=False, using=None):
        self.content_show = mark_safe(
            markdown.markdown(force_unicode(self.content), ['codehilite'], safe_mode='escape'))
        super(Wiki, self).save()


class PicType(models.Model):
    """the picture categories"""
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500, null=True)
    add_time = models.DateTimeField(auto_now=True)
    img = models.IntegerField(null=True)  # id for pic

    def getPicCount(self):
        return MyPic.objects.filter(type=self.id).count()

    def getPic(self):
        return Pic.objects.get(pk=self.img)

    class Meta:
        db_table = 'pic_type'


class Pic(models.Model):
    """picture"""
    img = models.CharField(max_length=200)
    key = models.CharField(max_length=200)  # qiniu key
    add_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pic'


class MyPic(models.Model):
    """my picture"""
    type = models.IntegerField()
    img = models.IntegerField(null=True)  # id for pic
    desc = models.CharField(max_length=500, null=True)
    add_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    def getType(self):
        return PicType.objects.get(pk=self.type)

    def getPic(self):
        return Pic.objects.get(pk=self.img)

    class Meta:
        db_table = 'mypic'


class Word(models.Model):
    status = models.IntegerField(default=0)  # 0:None; 1:Ok
    add_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'word'


class Words(models.Model):
    word = models.ForeignKey(Word)
    english = models.CharField(max_length=100)  # 0:None; 1:Ok
    explain = models.CharField(max_length=300, null=True)
    phonetic = models.CharField(max_length=100, null=True)  # 英标
    seq = models.CharField(max_length=300, null=True)
    add_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)  # ok

    class Meta:
        db_table = 'words'