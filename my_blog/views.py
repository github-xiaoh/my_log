from django.shortcuts import render,get_object_or_404

from django.http import HttpResponseRedirect, Http404

from django.core.urlresolvers import reverse

from .models import Topic,Entry

from .forms import TopicForm,EntryForm

from django.contrib.auth.decorators import login_required


def index(request):
    """学习笔记打主页"""
    return render(request,'my_blog/index.html')



def file_input(request):
    if request.method == 'GET':
        a = {'a':'开始上传'}
        return render(request, "my_blog/file_input.html",a)
    else:

        # with open('my_blog/file') as f:
        file_name = request.FILES.get('file_inputname')
        a = {'a': file_name+"上传成功"}

        return render(request,"my_blog/file_input.html",a)

# from django.views import View
#
# class file_input(View):
#     def get(self,request):
#         return render(request,"my_blog/file_input.html")
#     def post(self,request):
#         a = {'a':"返回"}
#         return render(request,"my_blog/file_input.html",a)



@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'my_blog/topics.html',context)




@login_required
def topic(request,topic_id):
    """显示单个主题及其所有的条目"""
    topic = get_object_or_404(Topic,id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries': entries}
    return render(request, 'my_blog/topic.html',context)





@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据,对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('my_blog:topics'))
    context = {'form': form}
    return render(request, 'my_blog/new_topic.html', context)




@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # 未提交数据,创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据,对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('my_blog:topic',args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'my_blog/new_entry.html', context)





@login_required
def edit_entry(request,entry_id):
    """编辑条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_blog:topic',args=[topic.id]))
    
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'my_blog/edit_entry.html',context)









# Create your views here.
