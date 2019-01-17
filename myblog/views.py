from django.shortcuts import render, get_object_or_404
from . models import Post,Category,Tag
import markdown
from django.views.generic import ListView,DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q

def First(request):
    return render(request,'first.html')

def search(request):
    q=request.GET.get('q')
    error_msg=''
    if not q:
        error_msg="请输入关键词"
        return render(request, 'index.html', {'error_msg':error_msg})
    post_list=Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request, 'index.html', {'error_msg':error_msg, 'post_list':post_list})
# Create your views here.
def index(request):
    post_list = Post.objects.all()
    return render(request, 'index.html', context={'post_list': post_list})
class IndexView(ListView):
    model=Post
    template_name= 'index.html'
    context_object_name='post_list'
    paginate_by=10
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        paginator=context.get('paginator')
        page=context.get('page_obj')
        is_paginated=context.get('is_paginated')
        pagination_data=self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return{ }
        left=[]
        right=[]
        left_has_more=False
        right_has_more=False
        first=False
        last=False
        page_number=page.number
        total_pages=paginator.num_pages
        page_range=paginator.page_range
        if page_number==1:
            right=page_range[page_number:page_number+2]
            if right[-1]<total_pages-1:
                right_has_more=True
            if right[-1]<total_pages:
                last=True
        elif page_number==total_pages:
            left=page_range[(page_number-3)if(page_number-3)>0 else 0:page_number-1]
            if left[0]>2:
                left_has_more=True
            if left[0]>1:
                first=True
        else:
            left=page_range[(page_number-3)if(page_number-3)>0 else 0:page_number-1]
            right=page_range[page_number:page_number+2]
            if right[-1]<total_pages-1:
                right_has_more=True
            if right[-1]<total_pages:
                last=True
            if left[0]>2:
                left_has_more=True
            if left[0]>1:
                first=True
        data={
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
        }
        return data

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量 +1
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    return render(request, 'myblog/detail.html')


# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'myblog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post


def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return render(request, 'index.html', context={'post_list':post_list})

class ArchivesView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'index.html', context={'post_list': post_list})

class CategoryView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)



class TagView(ListView):
    model=Post
    template_name= 'index.html'
    context_object_name='post_list'
    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)

def about(request):
    return render(request,'myblog/about.html')
def talking(request):
    return render(request,'myblog/talking.html')


