#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from django.http.response import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(CreateView)
from django.contrib.auth.decorators import login_required
from .models import Post, Comentario
from apps.blog.forms import FormComentario, FormPost

# Create your views here.
def index(request):
    ultimosposts=Post.objects.all().order_by('fecha_publicacion').reverse()[:3]
    return render(request, 'index.html', {'ultimosposts':ultimosposts})


def lista_posts(request):
    #posts = Post.objects.filter(fecha_publicacion=timezone.now()).order_by('fecha_publicacion')
    posts=Post.objects.all().order_by('fecha_publicacion')
    return render(request, 'posts.html',{'posts':posts})


def lista_categorias(request, categoria):
    posts = Post.objects.filter(
        categories__name__contains=categoria
    ).order_by("-fecha_creacion")
    context = {
        "categoria": categoria,
        "posts": posts,
        
    }
    return render(request, "blog/lista_categorias.html", context) 

class CreatePostView(CreateView, LoginRequiredMixin):
    login_url= '/login'
    #redirect_field_name='index_detail.html'

    form_class = FormPost

    model = Post

def postdetalle(request,id):
    try:
        data = Post.objects.get(id=id)
        comentarios = Comentario.objects.filter(aprobado=True)
        form = FormComentario()
        if request.method == "POST":
            form = FormComentario(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.post = data
                comentario.save()
                return redirect('post_detalle', id=data.id)
    except Post.DoesNotExist:
        raise Http404('El Post seleccionado no existe.')
    
    comentarios = Comentario.objects.all()
    context={
        "post": data,
        "comentarios": comentarios,
        "form": FormComentario()
    }
    return render(request, 'post_detalle.html', context)

def contacto(request):
    return render(request, 'contacto.html')

@login_required
def publicar_post(request, id):
    try:
        post =Post.objects.get(id =id)
    except Post.DoesNotExist:
        raise Http404('No existe el post seleccionado')
    post.publicar()
    return redirect('post_detail', id=id)


@login_required
def aprobar_comentario(request, id):
    try:
        comment =Comentario.objects.get(id =id)
    except Comentario.DoesNotExist:
        raise Http404('Comentario no existe')
    comment.aprobarComentario()
    return redirect('post_detalle', id=comment.post.id)


@login_required
def eliminar_comentario(request, id):
    try:
        comment =Comentario.objects.get(id =id)
    except Comentario.DoesNotExist:
        raise Http404('No existe Comentario')
    post_id = comment.post.id
    comment.eliminarComentario()
    return redirect('post_detalle', id=post_id)




''' def home_view(request):
    return HttpResponse("Esto es una página de prueba!")

def index(request):
    return render(request, 'inicio.html')

class IndexView(View):
    def get(self, request):
        return HttpResponse("Esta es la página principal")

class AboutView(TemplateView):
    #pass
    template_name = 'inicio.html'
'''


