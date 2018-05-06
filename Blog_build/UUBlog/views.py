#-*- coding:utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time,datetime
from django.db.models import Q
from django.db import connection
from django.template import RequestContext 

from UUBlog.models import Category, Article, PicType, MyPic, Pic
import simplejson as json
from django.views.generic.base import TemplateView
from django import forms
from django.forms import ModelForm
import common

import qiniu.conf
import qiniu.rs
import qiniu.io
import datetime
from PIL import Image
import StringIO
from django.conf import settings

# 初始化七牛环境
qiniu.conf.ACCESS_KEY = settings.QINIU_ACCESS_KEY
qiniu.conf.SECRET_KEY = settings.QINIU_SECRET_KEY

#上传凭证
policy = qiniu.rs.PutPolicy(settings.QINIU_BUCKET_NAME)
uptoken = policy.token()


def my_render_to_response(request,templateName,locals):
    return render_to_response(templateName,locals,context_instance=RequestContext(request))

def GetPostData(request,key,default=""):
    if request.POST.has_key(key):
        return request.POST[key]
    return default

def login(request):
    return True

def logout(request):
    return False

def home(request):
    viewsTopArticles=common.viewsTopArticles()
    remarkTopArticles=common.remarkTopArticles()
    newTopArticles=common.newTopArticles()
    categoryList=common.categoryList()

    articleList=Article.objects.order_by("-createtime").all()

    return my_render_to_response(request,"home.html",locals())
    #return HttpResponse(html)

def show(request,aid):
    viewsTopArticles=common.viewsTopArticles()
    remarkTopArticles=common.remarkTopArticles()
    newTopArticles=common.newTopArticles()
    categoryList=common.categoryList()

    articleInfo=Article.objects.get(id=aid)
    title=articleInfo.title
    content=articleInfo.content
    articleInfo.views+=1
    if not articleInfo.createtime:
        articleInfo.createtime=datetime.datetime.now()

    articleInfo.save()

    return my_render_to_response(request,"articleshow.html",locals())

def add(request):
    viewsTopArticles=common.viewsTopArticles()
    remarkTopArticles=common.remarkTopArticles()
    newTopArticles=common.newTopArticles()
    categoryList=common.categoryList()

    if request.POST.has_key('ok'):
        category=Category.objects.get(id=GetPostData(request,'category'))
        title = GetPostData(request,'title')
        pic = GetPostData(request,'pic')
        tags=GetPostData(request,'tags')
        summary=GetPostData(request,'summary')
        content = GetPostData(request,'content')
        
        if len(summary)==0:
            summary=summary[1:80] if len(summary)>80 else summary

        articleInfo = Article(category=category,
                              title = title,
                              pic="",
                              tags=tags,
                              summary=summary,
                              content = content,
                              createtime=datetime.datetime.now(),
                              views=0,
                              comments=0,
                              goods=0,
                              bads=0,
                              status=1,
                              user_id=1,
                              user_name="admin")
        articleInfo.save()

        return HttpResponseRedirect('/')
    else:
        return my_render_to_response(request,"addarticle.html",locals())
    


def edit(request,aid):
    viewsTopArticles=common.viewsTopArticles()
    remarkTopArticles=common.remarkTopArticles()
    newTopArticles=common.newTopArticles()
    categoryList=common.categoryList()


    if request.POST.has_key('ok'):
        articleInfo=Article.objects.get(id=aid)
        
        articleInfo.category=Category.objects.get(id=GetPostData(request,'category'))
        articleInfo.title = GetPostData(request,'title')
        articleInfo.pic = GetPostData(request,'pic')
        articleInfo.tags=GetPostData(request,'tags')
        articleInfo.summary=GetPostData(request,'summary')
        articleInfo.content = GetPostData(request,'content')

        articleInfo.save()

        return HttpResponseRedirect('/')
    else:
        articleInfo=Article.objects.get(id=aid)
        title=articleInfo.title
        content=articleInfo.content
        return my_render_to_response(request,"editarticle.html",locals())


def category(request,action="",cid=-1):
    viewsTopArticles=common.viewsTopArticles()
    remarkTopArticles=common.remarkTopArticles()
    newTopArticles=common.newTopArticles()
    categoryList=common.categoryList()
    

    if request.POST.has_key('ok'):
        name = request.POST['name']
        if cid!=-1:
            categoryInfo=Category(name=name)
        else:
            categoryInfo=Category.objects.get(id=cid)
            categoryInfo.name=name
        categoryInfo.save()

        return HttpResponseRedirect('/')
    else:

        return my_render_to_response(request,"category.html",locals())

def action(request,action):
    if action=="edit":
        aaa=1

class BaseRequest:
    def GetPost(self,article):
            title = article['title']
            content = article['content']
            tags = article['tags']
            times = time.time()
            cate_id = int(request.POST['category'])

def aaa(request):
    if not editId:
        if request.POST.has_key('ok'):
            caption = request.POST['caption']
            shortContent = request.POST['description']
            content = request.POST['content']
            tags = request.POST['tags']
            times = time.time()
            cate_id = int(request.POST['category'])
            if caption and shortContent:
                addArticle = Models.Article(caption = caption,shortContent = shortContent,
                            content = content,tags = tags,times = times,degree = 1,
                            cate_id = cate_id)
                addArticle.save()
                return HttpResponseRedirect('/addArticle/')
    else:#编辑文章
        article = Models.Article.objects.filter(id = int(editId)).values('cate_id','tags',
                'caption','content','shortContent')
        caption =  article[0]['caption']
        content = article[0]['content']
        cateId = article[0]['cate_id']
        tags = article[0]['tags']
        description = article[0]['shortContent']
        if request.POST.has_key('ok'):
            caption = request.POST['caption']
            shortContent = request.POST['description']
            content = request.POST['content']
            tags = request.POST['tags']
            times = time.time()
            cate_id = int(request.POST['category'])
            if caption and shortContent:
                Models.Article.objects.filter(id = editId).update(caption = caption,
                            shortContent = shortContent,content = content,tags = tags,
                            cate = cate_id)
                return HttpResponseRedirect('/addArticle/?action='+editId)
    return render_to_response('admin/addArticle.html',locals())


class MyBaseView(TemplateView):

    def __init__(self,request):
        self.request=request

    def my_render_to_response(self,templateName,locals):
        return render_to_response(templateName,locals,context_instance=RequestContext(self.request))

    def home(self):
        adf=5

    def add(self):
        aaa=0

    def update(self):
        asdfasfd=2

    def delete(self,id):
        aaa=""

    def getPostData(self,key):
        if self.request.POST.has_key(key):
            return self.request.POST[key]
        return ''
    def hasPostData(self,key):
        return self.request.POST.has_key(key)

class ArticleView(MyBaseView):

    def __init__(self, request):
        return super(ArticleView, self).__init__(request)

    def add(self):

        if self.hasPostData('ok'):

                title =self.getPostData('title')
                content = self.getPostData('content')

                category=Category.objects.get(id=1)
                createtime=datetime.datetime.now()
                views=0

                addArticle = Article(title = title,content = content,category=category,createtime=createtime,views=views)
                addArticle.save()

                return HttpResponseRedirect('/')

        return MyBaseView.my_render_to_response(self,request,"addarticle.html",locals())

############################################################################################
def ajax_ok_data(data='', next=None, message=None):
    return ajax_data('ok', data=data, next=next, message=message)


def json_ok_data(data='', message=None):
    return json_data(ajax_data('ok', data=data))


def json_data(data, check=False):
    encode = settings.DEFAULT_CHARSET
    if check:
        if not is_ajax_data(data):
            raise SimpleAjaxException, 'Return data should be follow the Simple Ajax Data Format'
    return simplejson.dumps(uni_str(data, encode))


def ajax_fail_data(error='', next=None, message=None):
    return ajax_data('fail', error=error, next=next, message=message)


def ajax_ok(data='', next=None, message=None):
    """
    return a success response
    """

    return json_response(ajax_ok_data(data, next, message))


def ajax_fail(error='', next=None, message=None):
    """
    return an error response
    """

    return json_response(ajax_fail_data(error, next, message))


def json(data, check=False):
    encode = settings.DEFAULT_CHARSET
    if check:
        if not is_ajax_data(data):
            raise SimpleAjaxException, 'Return data should be follow the Simple Ajax Data Format'
    return simplejson.dumps(uni_str(data, encode))


def json_response(data, check=False):
    encode = settings.DEFAULT_CHARSET

    if check:
        if not is_ajax_data(data):
            raise SimpleAjaxException, 'Return data should be follow the Simple Ajax Data Format'
    try:
        return HttpResponse(simplejson.dumps(uni_str(data, encode)))
    except:
        return HttpResponse(simplejson.dumps(uni_str(data, "gb2312")))


def ajax_data(response_code, data=None, error=None, next=None, message=None):
    """if the response_code is true, then the data is set in 'data',
    if the response_code is false, then the data is set in 'error'
    """

    r = dict(response='ok', data='', error='', next='', message='')
    if response_code is True or response_code.lower() in ('ok', 'yes', 'true'):
        r['response'] = 'ok'
    else:
        r['response'] = 'fail'
    if data:
        r['data'] = data
    if error:
        r['error'] = error
    if next:
        r['next'] = next
    if message:
        r['message'] = message
    return r


def is_ajax_data(data):
    """Judge if a data is an Ajax data"""

    if not isinstance(data, dict): return False
    for k in data.keys():
        if not k in ('response', 'data', 'error', 'next', 'message'): return False
    if not data.has_key('response'): return False
    if not data['response'] in ('ok', 'fail'): return False
    return True


def uni_str(a, encoding=None):
    if not encoding:
        encoding = settings.DEFAULT_CHARSET

    if isinstance(a, (list, tuple)):

        s = []
        for i, k in enumerate(a):
            s.append(uni_str(k, encoding))
        return s
    elif isinstance(a, dict):

        s = {}
        for i, k in enumerate(a.items()):
            key, value = k
            s[uni_str(key, encoding)] = uni_str(value, encoding)
        return s
    elif isinstance(a, unicode):

        return a
    elif isinstance(a, (int, float)):

        return a
    elif isinstance(a, str) or (hasattr(a, '__str__') and callable(getattr(a, '__str__'))):

        if getattr(a, '__str__'):
            a = str(a)

        return unicode(a, encoding)
    else:
        return a


def get_options_data(data):
    """
    return select element's options
    """

    retval = ''
    for item in data:
        retval = retval + item.__option__() + ","

    return retval[0:-1]


class SuperQiniu(object):
    def __init__(self, filepath, w=200, h=200, request=None, **kwargs):
        self.filepath = filepath    # 文件绝对路径
        self.key = datetime.datetime.now()               # 文件唯一标示
        self.request = request
        self.w = w      # 宽度
        self.h = h      # 高度
        self.kwargs = kwargs

    def uploadFile(self):
        """上传图片"""
        extra = qiniu.io.PutExtra()
        mime_type = self.filepath.content_type
        extra.mime_type = mime_type
        type = 'PNG'
        if mime_type == 'image/jpeg':
            type = 'JPEG'
        self.filepath.seek(0)
        resize_pic = self.setPic(type)
        ret, err = qiniu.io.put(uptoken, str(self.key), resize_pic, extra)
        if err is not None:
            print 'error:', err
            return
        return settings.QINIU_DOMAIN+'/'+ret['key']

    def downloadFile(self):
        """下载图片"""
        base_url = qiniu.rs.make_base_url(settings.QINIU_DOMAIN, str(self.key))
        policy = qiniu.rs.GetPolicy()
        private_url = policy.make_request(base_url)
        return private_url


    def setPic(self, type):
        """设置w*h大小图片"""
        image = Image.open(self.filepath)
        image.thumbnail((self.w, self.h), Image.ANTIALIAS)
        image_file = StringIO.StringIO()
        image.save(image_file, type, quality=90)
        image_file.seek(0)
        return image_file

    def delFile(self):
        """delete picture"""
        key = self.filepath     # 此时表示图片key 而非路径
        if key:
            ret, err = qiniu.rs.Client().delete(settings.QINIU_BUCKET_NAME, key)
            if err is not None:
                print 'error: %s ' % err
                return
        return


    def delMoreFiles(self):
        """批量删除图片"""
        remoteFile = []
        for obj in self.filepath:       # 此时filepath表示keys列表集合
            remoteFile.append(qiniu.rs.EntryPath(settings.QINIU_BUCKET_NAME, obj))
        if remoteFile:
            rets, err = qiniu.rs.Client().batch_delete(remoteFile)
            if not [ret['code'] for ret in rets] == [200, 200]:
                print 'error: %s ' % "删除失败"
                return
        return

    def getKey(self):
        """return key"""
        return self.key







class PicTypeForm(ModelForm):
    """pictype form"""
    title = forms.CharField(max_length=100, label=u'title', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'title', 'required': ''})
    )
    desc = forms.CharField(label=u'wiki',widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': u'describe'})
    )

    def clean(self):
        cleaned_data = super(PicTypeForm, self).clean()
        title = cleaned_data.get('title').strip()

        if not title and PicType.objects.filter(title__icontains=title).exists():
            raise forms.ValidationError(u'该分类已存在')
        return cleaned_data

    class Meta:
        model = PicType
        fields = ('title', 'desc')


class MypicForm(ModelForm):
    """MypicForm form"""
    type = forms.ModelChoiceField(queryset=PicType.objects.order_by('-id'), widget=forms.RadioSelect)
    desc = forms.CharField(label=u'wiki',widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': u'describe'})
    )

    class Meta:
        model = MyPic
        fields = ('type', 'desc')



def pic(request):
    """pic index"""
    context = {}
    context['pics'] = PicType.objects.order_by('-id')
    return render(request, 'pic/index.html', context)


def picView(request, id):
    """view picture for this category."""
    context = {}
    context['type'] = PicType.objects.get(pk=id)
    context['pics'] = MyPic.objects.filter(type=id).order_by('-id')
    return render(request, 'pic/pic.html', context)

def UploadPic(request):
    """upload pic to qiniu."""
    if request.method == 'POST':
        img = request.FILES.get('Filedata', None)
        type = request.POST.get('type', None)
        if type:
            qn = SuperQiniu(img, w=800, h=520)
        else:
            qn = SuperQiniu(img)
        qn.uploadFile()
        remote_url = qn.downloadFile()
        key = qn.getKey()
        pic = Pic.objects.create(img=remote_url, key=key)
        return ajax_ok({'id':pic.id, 'url':pic.img, 'key':key})



def CreatePicType(request):
    """create the type of picture"""
    context = {}
    if request.method == 'POST':
        id = int(request.POST.get('id', 0))
        if id:
            pictype =get_object_or_404(PicType, pk=id)
            form = PicTypeForm(request.POST, instance=pictype)
        else:
            form = PicTypeForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            img = request.POST.get('pid')
            f.img = img
            f.save()
            return HttpResponseRedirect('/pic/')
        context['form'] = form

    else:
        id = request.GET.get('id', None)
        form = PicTypeForm()
        if id:
            pictype =get_object_or_404(PicType, pk=id)
            context['img_obj'] = pictype.getPic()
            form = PicTypeForm(instance=pictype)
        context['form'] = form
        context['id'] = id

    return render(request, 'pic/addtype.html', context)


def UploadMyPic(request, id):
    """create the type of picture"""
    context = {}
    if request.method == 'POST':
        data = request.POST.get('data')
        data = json.loads(data)

        for obj in data:
            MyPic.objects.create(type=id, img=obj['pid'], desc=obj['desc'])
        return HttpResponse('ok')

    else:
        pictype =get_object_or_404(PicType, pk=id)
        context['pictype'] = pictype

    return render(request, 'pic/addpic.html', context)



def edit_mypic(request):
    """edit mypic"""
    if request.method == 'POST':
        id = request.POST.get('id')
        desc = request.POST.get('desc', '')
        MyPic.objects.filter(pk=id).update(desc=desc)
        return HttpResponse('ok')





