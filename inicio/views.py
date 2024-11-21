# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Post
import subprocess, json


def home(request):
    return render(request, 'home.html')

def rule(request):
    return render(request, 'rule.html')

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        content_markdown = data.get('content_markdown')

        if not title or not content_markdown:
            return JsonResponse({'error': 'Título y contenido son requeridos.'}, status=400)

        post = Post.objects.create(
            title=title,
            content_markdown=content_markdown
        )
        return JsonResponse({'id': post.id, 'title': post.title}, status=201)
@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all().values('id', 'title', 'content_markdown')
        return JsonResponse(list(posts), safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.create(
            title=data['title'],
            content_markdown=data['content_markdown']
        )
        return JsonResponse({'id': post.id, 'title': post.title}, status=201)

@csrf_exempt
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        return JsonResponse({
            'id': post.id,
            'title': post.title,
            'content_markdown': post.content_markdown
        })

    if request.method == 'PUT':
        data = json.loads(request.body)
        post.title = data['title']
        post.content_markdown = data['content_markdown']
        post.save()
        return JsonResponse({'id': post.id, 'title': post.title})



def editor_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Article.objects.create(title=title, content=content)
        return redirect("article_list") 

    return render(request, 'editor.html')
# views.py

def lista_articulos(request):
    articulos = Article.objects.all()
    return render(request, 'articulos.html', {'articulos': articulos})

def dashboard(request):
    return render(request, 'dashboard.html')

